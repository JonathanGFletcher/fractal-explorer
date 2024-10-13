package render

import (
	"errors"
	"fmt"
	"image"
	"image/color"
	"image/png"
	"math"
	"math/rand"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/jonathangfletcher/fractal-explorer/server/models"
	"gocv.io/x/gocv"
	"gorm.io/gorm"
)

func ProgressValue(start float64, end float64, ratio float64) float64 {
	increment := (end - start) * ratio
	return start + increment
}

func NewFractalJulia(request models.RequestFractalJulia) (*image.RGBA, error) {
	if request.Dimensions.MaxX-request.Dimensions.MinX > request.Dimensions.Width || request.Dimensions.MaxY-request.Dimensions.MinY > request.Dimensions.Height {
		return nil, errors.New("invalid dimensions")
	}
	if request.Dimensions.MaxX-request.Dimensions.MinX < 0 || request.Dimensions.MaxY-request.Dimensions.MinY < 0 {
		return nil, errors.New("invalid dimensions")
	}

	topLeft := image.Point{request.Dimensions.MinX, request.Dimensions.MinY}
	bottomRight := image.Point{request.Dimensions.MaxX, request.Dimensions.MaxY}
	img := image.NewRGBA(image.Rectangle{topLeft, bottomRight})

	for y := request.Dimensions.MinY; y <= request.Dimensions.MaxY; y++ {
		for x := request.Dimensions.MinX; x <= request.Dimensions.MaxX; x++ {
			renderScale := 1.0 / request.Scale / float64(request.Dimensions.Height) * 2.5
			pixelColorValue := models.Vector3F{
				X: 0.0,
				Y: 0.0,
				Z: 0.0,
			}
			for s := request.Samples; s != 0; s-- {
				px := (float64(x-request.Dimensions.Width/2)+(rand.Float64()*2-1))*renderScale + request.Center.X
				py := (float64(y-request.Dimensions.Height/2)+(rand.Float64()*2-1))*renderScale + request.Center.Y
				pixel := models.Vector2F{
					X: px,
					Y: py,
				}

				zn := pixel
				it := 0.0
				for {
					constant
					constant
					constant
					constant	it++
				}
				mod := math.Sqrt(zn.X*zn.X + zn.Y*zn.Y)
				iterations := it - math.Log2(math.Max(1.0, math.Log2(mod)))
				value := iterations / float64(request.Iterations)
				pixelColorValue = pixelColorValue.Add(GetColorValue(value, request.Colors))
			}

			pixelColor := color.RGBA{
				R: uint8(pixelColorValue.X * 255 / float64(request.Samples)),
				G: uint8(pixelColorValue.Y * 255 / float64(request.Samples)),
				B: uint8(pixelColorValue.Z * 255 / float64(request.Samples)),
				A: 255,
			}
			img.Set(x, y, pixelColor)
		}
	}

	return img, nil
}

func NewFractalImageJulia(request models.RequestFractalJulia) (string, error) {
	filename := models.NewFractalJuliaFilename(request, "", "png")
	path := "/media/" + filename
	url := "/api/static/" + filename
	file, err := os.Open(path)
	if err == nil {
		file.Close()
		return url, nil
	}

	request.Colors = DefaultColors()
	img, err := NewFractalJulia(request)
	if err != nil {
		return "", err
	}
	file, err = os.Create(path)
	if err != nil {
		return "", err
	}
	png.Encode(file, img)
	file.Close()
	return url, nil
}

func NewFractalVideoJulia(request models.RequestFractalJuliaVideo, c *gin.Context, db *gorm.DB) (string, error) {
	id, err := uuid.NewV7()
	if err != nil {
		return "", err
	}
	filename := id.String() + ".avi"
	path := "/media/" + filename

	var frames []models.RequestFractalJulia
	numFrames := request.Seconds * 30
	for i := 0; i <= int(numFrames); i++ {
		ratio := float64(i) / float64(numFrames)
		constant := models.Vector2F{
			X: ProgressValue(request.Start.Constant.X, request.End.Constant.X, ratio),
			Y: ProgressValue(request.Start.Constant.Y, request.End.Constant.Y, ratio),
		}
		center := models.Vector2F{
			X: ProgressValue(request.Start.Constant.X, request.End.Constant.X, ratio),
			Y: ProgressValue(request.Start.Constant.Y, request.End.Constant.Y, ratio),
		}
		scale := math.Pow(ProgressValue(math.Log2(request.Start.Scale), math.Log2(request.End.Scale), ratio), 2)
		iterations := int(ProgressValue(float64(request.Start.Iterations), float64(request.End.Iterations), ratio))

		r := models.RequestFractalJulia{
			Power:      request.Start.Power,
			Constant:   constant,
			Center:     center,
			Scale:      scale,
			Iterations: iterations,
			Samples:    request.Start.Samples,
			Dimensions: request.Start.Dimensions,
			Colors:     DefaultColors(),
		}
		frames = append(frames, r)
	}

	db.Create(&models.VideoTask{
		SessionId:       id.String(),
		Completed:       false,
		TotalFrames:     len(frames),
		CompletedFrames: 0,
	})

	go func() {
		vw, err := gocv.VideoWriterFile(path, "MJPG", 30, request.Start.Dimensions.Width, request.Start.Dimensions.Height, true)
		if err != nil {
			fmt.Errorf("Video %s: Error: %s\n", id.String(), err.Error())
			return
		}
		defer vw.Close()

		for i, r := range frames {
			frameNumber := i + 1
			img, err := NewFractalJulia(r)
			if err != nil {
				fmt.Errorf("Video %s: Error: %s\n", id.String(), err.Error())
				return
			}
			mat, err := gocv.ImageToMatRGBA(img)
			if err != nil {
				fmt.Errorf("Video %s: Error: %s\n", id.String(), err.Error())
				return
			}
			defer mat.Close()
			err = vw.Write(mat)
			if err != nil {
				fmt.Errorf("Video %s: Error: %s\n", id.String(), err.Error())
				return
			}
			var task models.VideoTask
			result := db.Find(&task, "session_id = ?", id.String())
			if result.Error != nil {
				fmt.Errorf("Video %s: Error: %s\n", id.String(), result.Error.Error())
				return
			}
			task.CompletedFrames = frameNumber
			db.Save(&task)
			fmt.Printf("Video %s: Rendered %d/%d frames\n", id.String(), frameNumber, len(frames))
		}
		var task models.VideoTask
		result := db.Find(&task, "session_id = ?", id.String())
		if result.Error != nil {
			fmt.Errorf("Video %s: Error: %s\n", id.String(), result.Error.Error())
			return
		}
		task.Completed = true
		db.Save(&task)
		fmt.Printf("Video %s: Completed\n", id.String())
	}()

	return id.String(), nil
}
