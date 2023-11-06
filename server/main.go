package main

import (
	"github.com/gin-gonic/gin"
	"github.com/jonathangfletcher/fractal-explorer/server/routes"
)

func main() {

	router := gin.Default()
	router.SetTrustedProxies([]string{"127.0.0.1"})

	router.GET("/julia", func(ctx *gin.Context) { routes.Julia(ctx) })
	router.GET("/mandelbrot", func(ctx *gin.Context) { routes.Mandelbrot(ctx) })

	router.Run(":80")
}
