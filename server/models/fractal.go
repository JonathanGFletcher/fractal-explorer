package models

import "fmt"

type Vector2F struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
}

func (a *Vector2F) Add(b Vector2F) Vector2F {
	return Vector2F{
		X: a.X + b.X,
		Y: a.Y + b.Y,
	}
}

type Vector3F struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
	Z float64 `json:"z"`
}

func (a *Vector3F) Add(b Vector3F) Vector3F {
	return Vector3F{
		X: a.X + b.X,
		Y: a.Y + b.Y,
		Z: a.Z + b.Z,
	}
}

type ColorStep struct {
	Value float64  `json:"value" binding:"required"`
	Color Vector3F `json:"color" binding:"required"`
}

type FractalDimensions struct {
	Width  int `json:"width" binding:"required"`
	Height int `json:"height" binding:"required"`
	MinX   int `json:"min_x"`
	MinY   int `json:"min_y"`
	MaxX   int `json:"max_x" binding:"required"`
	MaxY   int `json:"max_y" binding:"required"`
}

type RequestFractalJulia struct {
	Constant   Vector2F          `json:"constant" binding:"required"`
	Center     Vector2F          `json:"center" binding:"required"`
	Scale      float64           `json:"scale" binding:"required"`
	Iterations int               `json:"iterations" binding:"required"`
	Samples    int               `json:"samples" binding:"required"`
	Dimensions FractalDimensions `json:"dimensions" binding:"required"`
	Colors     []ColorStep       `json:"colors" binding:"required"`
}

type RequestFractalMandelbrot struct {
	Constant   Vector2F          `json:"constant" binding:"required"`
	Center     Vector2F          `json:"center" binding:"required"`
	Scale      float64           `json:"scale" binding:"required"`
	Iterations int               `json:"iterations" binding:"required"`
	Samples    int               `json:"samples" binding:"required"`
	Dimensions FractalDimensions `json:"dimensions" binding:"required"`
	Colors     []ColorStep       `json:"colors" binding:"required"`
}

type ResponseFractal struct {
	Url string `json:"url"`
}

func NewFractalJuliaFilename(r RequestFractalJulia) string {
	return fmt.Sprintf("%f_%f_%f_%f_%f_%d_%d_%d_%d_%d_%d_%d_%d.png", r.Constant.X, r.Constant.Y, r.Center.X, r.Center.Y, r.Scale, r.Iterations, r.Samples, r.Dimensions.Width, r.Dimensions.Height, r.Dimensions.MinX, r.Dimensions.MinY, r.Dimensions.MaxX, r.Dimensions.MaxY)
}
