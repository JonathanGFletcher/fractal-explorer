package routes

import (
	"net/http"

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

	img, err := render.NewFractalJulia(request)
	if err != nil {
		c.AbortWithError(http.StatusBadRequest, err)
	}
}

func Mandelbrot(c *gin.Context) {

}
