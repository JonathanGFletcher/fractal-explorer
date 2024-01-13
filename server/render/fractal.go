package render

import (
	"errors"
	"image"
	"image/color"
	"math"
	"math/rand"

	"github.com/jonathangfletcher/fractal-explorer/server/models"
)

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
					if !((zn.X*zn.X+zn.Y*zn.Y) < 4.0 && it < float64(request.Iterations)) {
						break
					}
					r := math.Sqrt(zn.X*zn.X + zn.Y*zn.Y)
					t := math.Atan2(zn.Y, zn.X)
					z := models.Vector2F{
						X: math.Pow(r, float64(request.Power)) * math.Cos(float64(request.Power)*t),
						Y: math.Pow(r, float64(request.Power)) * math.Sin(float64(request.Power)*t),
					}
					zn = z.Add(request.Constant)
					it++
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
