package routes

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/jonathangfletcher/fractal-explorer/server/models"
	"github.com/jonathangfletcher/fractal-explorer/server/render"
	"gorm.io/gorm"
)

func Julia(c *gin.Context, db *gorm.DB) {
	var request models.RequestFractalJulia
	err := c.BindJSON(&request)
	if err != nil {
		c.AbortWithError(http.StatusBadRequest, err)
		return
	}

	url, err := render.NewFractalImageJulia(request)
	if err != nil {
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	c.JSON(http.StatusOK, models.ResponseFractal{
		Url: url,
	})
}

func JuliaVideoStart(c *gin.Context, db *gorm.DB) {
	var request models.RequestFractalJuliaVideo
	err := c.BindJSON(&request)
	if err != nil {
		c.AbortWithError(http.StatusBadRequest, err)
		return
	}
	id, err := render.NewFractalVideoJulia(request, c, db)
	if err != nil {
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}
	c.JSON(http.StatusOK, models.ResponseFractalStartVideo{
		Id: id,
	})
}

func JuliaVideoStatus(c *gin.Context, db *gorm.DB) {

}

func Mandelbrot(c *gin.Context, db *gorm.DB) {
	// WIP
}

func MandelbrotStartVideo(c *gin.Context, db *gorm.DB) {
	// WIP
}
