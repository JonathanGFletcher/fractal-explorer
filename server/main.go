package main

import (
	"github.com/gin-gonic/gin"
	"github.com/jonathangfletcher/fractal-explorer/server/database"
	"github.com/jonathangfletcher/fractal-explorer/server/routes"
)

func main() {

	router := gin.Default()
	router.SetTrustedProxies([]string{"127.0.0.1"})
	router.Static("/static", "/media")

	db := database.Connect()

	router.POST("/julia", func(ctx *gin.Context) { routes.Julia(ctx, db) })
	router.POST("/video/julia/start", func(ctx *gin.Context) { routes.JuliaVideoStart(ctx, db) })
	router.POST("/video/julia/status", func(ctx *gin.Context) { routes.JuliaVideoStatus(ctx, db) })
	router.POST("/mandelbrot", func(ctx *gin.Context) { routes.Mandelbrot(ctx, db) })

	router.Run(":80")
}
