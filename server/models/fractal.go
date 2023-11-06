package models

type Vector2F struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
}

type FractalDimensions struct {
	Width  int `json:"width"`
	Height int `json:"height"`
	MinX   int `json:"min_x"`
	MinY   int `json:"min_y"`
	MaxX   int `json:"max_x"`
	MaxY   int `json:"max_y"`
}

type RequestFractalJulia struct {
	Constant   Vector2F          `json:"constant"`
	Center     Vector2F          `json:"center"`
	Scale      float64           `json:"scale"`
	Iterations int               `json:"iterations"`
	Samples    int               `json:"samples"`
	Dimensions FractalDimensions `json:"dimensions"`
}

type RequestFractalMandelbrot struct {
	Constant   Vector2F          `json:"constant"`
	Center     Vector2F          `json:"center"`
	Scale      float64           `json:"scale"`
	Iterations int               `json:"iterations"`
	Samples    int               `json:"samples"`
	Dimensions FractalDimensions `json:"dimensions"`
}
