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

	request.Colors = render.DefaultColors()
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
	// WIP
}
