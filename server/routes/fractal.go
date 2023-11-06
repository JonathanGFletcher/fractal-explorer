package routes

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/jonathangfletcher/fractal-explorer/server/models"
)

func Julia(c *gin.Context) {
	var request models.RequestFractalJulia
	err := c.BindJSON(&request)
	if err != nil {
		c.AbortWithError(http.StatusBadRequest, err)
		return
	}
}

func Mandelbrot(c *gin.Context) {

}
