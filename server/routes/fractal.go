package routes

import (
	"image/png"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/jonathangfletcher/fractal-explorer/server/models"
	"github.com/jonathangfletcher/fractal-explorer/server/render"
)

func Julia(c *gin.Context) {
	var request models.RequestFractalJulia
	err := c.BindJSON(&request)
	if err != nil {
		c.AbortWithError(http.StatusBadRequest, err)
		return
	}

	filename := models.NewFractalJuliaFilename(request)
	path := "/media/" + filename
	url := "/api/static/" + filename
	file, err := os.Open(path)
	if err == nil {
		file.Close()
		c.JSON(http.StatusOK, models.ResponseFractal{
			Url: url,
		})
		return
	}

	steps := []models.ColorStep{}
	steps = append(steps, models.ColorStep{Value: 0.0, Color: models.Vector3F{X: 17.0 / 255.0, Y: 3.0 / 255.0, Z: 77.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.03, Color: models.Vector3F{X: 38.0 / 255.0, Y: 15.0 / 255.0, Z: 141.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.05, Color: models.Vector3F{X: 111.0 / 255.0, Y: 45.0 / 255.0, Z: 12.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.25, Color: models.Vector3F{X: 203.0 / 255.0, Y: 52.0 / 255.0, Z: 82.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.5, Color: models.Vector3F{X: 250.0 / 255.0, Y: 102.0 / 255.0, Z: 34.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.85, Color: models.Vector3F{X: 254.0 / 255.0, Y: 221.0 / 255.0, Z: 8.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.95, Color: models.Vector3F{X: 101.0 / 255.0, Y: 240.0 / 255.0, Z: 142.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 1.0, Color: models.Vector3F{X: 1.0, Y: 1.0, Z: 1.0}})
	request.Colors = steps

	img, err := render.NewFractalJulia(request)
	if err != nil {
		c.AbortWithError(http.StatusBadRequest, err)
	}
	file, err = os.Create(path)
	if err != nil {
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}
	png.Encode(file, img)
	file.Close()

	c.JSON(http.StatusOK, models.ResponseFractal{
		Url: url,
	})
}

func Mandelbrot(c *gin.Context) {

}
