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

	// steps := []models.ColorStep{}
	// steps = append(steps, models.ColorStep{Value: 0.0, Color: models.Vector3F{X: 17.0 / 255.0, Y: 3.0 / 255.0, Z: 77.0 / 255.0}})
	// steps = append(steps, models.ColorStep{Value: 0.03, Color: models.Vector3F{X: 38.0 / 255.0, Y: 15.0 / 255.0, Z: 141.0 / 255.0}})
	// steps = append(steps, models.ColorStep{Value: 0.05, Color: models.Vector3F{X: 111.0 / 255.0, Y: 45.0 / 255.0, Z: 12.0 / 255.0}})
	// steps = append(steps, models.ColorStep{Value: 0.25, Color: models.Vector3F{X: 203.0 / 255.0, Y: 52.0 / 255.0, Z: 82.0 / 255.0}})
	// steps = append(steps, models.ColorStep{Value: 0.5, Color: models.Vector3F{X: 250.0 / 255.0, Y: 102.0 / 255.0, Z: 34.0 / 255.0}})
	// steps = append(steps, models.ColorStep{Value: 0.85, Color: models.Vector3F{X: 254.0 / 255.0, Y: 221.0 / 255.0, Z: 8.0 / 255.0}})
	// steps = append(steps, models.ColorStep{Value: 0.95, Color: models.Vector3F{X: 101.0 / 255.0, Y: 240.0 / 255.0, Z: 142.0 / 255.0}})
	// steps = append(steps, models.ColorStep{Value: 1.0, Color: models.Vector3F{X: 1.0, Y: 1.0, Z: 1.0}})

	// start := time.Now()
	// img, _ := render.NewFractalJulia(models.RequestFractalJulia{
	// 	Constant:   models.Vector2F{X: -0.8, Y: 0.156},
	// 	Center:     models.Vector2F{X: 0.0, Y: 0.0},
	// 	Scale:      1.0,
	// 	Iterations: 500,
	// 	Samples:    4,
	// 	Dimensions: models.FractalDimensions{
	// 		Width:  3000,
	// 		Height: 2000,
	// 		MinX:   1500,
	// 		MinY:   0,
	// 		MaxX:   2999,
	// 		MaxY:   999,
	// 	},
	// 	Colors: steps,
	// })
	// end := time.Now()
	// elapsed := end.Sub(start)
	// fmt.Println("Time elapsed: " + elapsed.String())
	// file, _ := os.Create("./test.png")
	// png.Encode(file, img)
	// file.Close()
}
