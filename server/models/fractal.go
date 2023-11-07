package models

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
	Value float64
	Color Vector3F
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
	Colors     []ColorStep       `json:"colors"`
}

type RequestFractalMandelbrot struct {
	Constant   Vector2F          `json:"constant"`
	Center     Vector2F          `json:"center"`
	Scale      float64           `json:"scale"`
	Iterations int               `json:"iterations"`
	Samples    int               `json:"samples"`
	Dimensions FractalDimensions `json:"dimensions"`
	Colors     []ColorStep       `json:"colors"`
}
