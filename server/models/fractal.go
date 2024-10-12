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
	Value float64  `json:"value"`
	Color Vector3F `json:"color"`
}

type FractalDimensions struct {
	Width  int `json:"width"`
	Height int `json:"height"`
	MinX   int `json:"view_min_x"`
	MinY   int `json:"view_min_y"`
	MaxX   int `json:"view_max_x"`
	MaxY   int `json:"view_max_y"`
}

type RequestFractalJulia struct {
	Power      int               `json:"power" binding:"required"`
	Constant   Vector2F          `json:"constant" binding:"required"`
	Center     Vector2F          `json:"center" binding:"required"`
	Scale      float64           `json:"scale" binding:"required"`
	Iterations int               `json:"iterations" binding:"required"`
	Samples    int               `json:"samples" binding:"required"`
	Dimensions FractalDimensions `json:"dimensions" binding:"required"`
	Colors     []ColorStep       `json:"colors" binding:"required"`
}

type RequestFractalJuliaVideo struct {
	Start   RequestFractalJulia `json:"start"`
	End     RequestFractalJulia `json:"end"`
	Seconds int                 `json:"seconds"`
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

type ResponseFractalStartVideo struct {
	Id string `json:"id"`
}

func NewFractalJuliaFilename(r RequestFractalJulia, prefix string, extension string) string {
	if prefix != "" {
		prefix += "_"
	}
	return fmt.Sprintf("%sp%d_kx%f_ky%f_cx%f_cy%f_sc%f_it%d_sa%d_dw%d_dh%d_dmix%d_dmiy%d_dmax%d_dmay%d.%s", prefix, r.Power, r.Constant.X, r.Constant.Y, r.Center.X, r.Center.Y, r.Scale, r.Iterations, r.Samples, r.Dimensions.Width, r.Dimensions.Height, r.Dimensions.MinX, r.Dimensions.MinY, r.Dimensions.MaxX, r.Dimensions.MaxY, extension)
}
