package main

import (
	"github.com/gin-gonic/gin"
	"github.com/jonathangfletcher/fractal-explorer/server/routes"
)

func main() {

	router := gin.Default()
	router.SetTrustedProxies([]string{"127.0.0.1"})
	router.Static("/static", "/media")

	router.POST("/julia", func(ctx *gin.Context) { routes.Julia(ctx) })
	router.POST("/mandelbrot", func(ctx *gin.Context) { routes.Mandelbrot(ctx) })

	router.Run(":80")
}
