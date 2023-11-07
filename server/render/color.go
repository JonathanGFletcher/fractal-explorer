package render

import (
	"github.com/jonathangfletcher/fractal-explorer/server/models"
)

func GetColorValue(value float64, steps []models.ColorStep) models.Vector3F {
	if value >= 1.0 {
		c := steps[len(steps)-1].Color
		return models.Vector3F{
			X: c.X,
			Y: c.Y,
			Z: c.Z,
		}
	} else if value <= 0.0 {
		c := steps[0].Color
		return models.Vector3F{
			X: c.X,
			Y: c.Y,
			Z: c.Z,
		}
	}

	var c models.Vector3F
	for i, step := range steps {
		if step.Value > value {
			ran := step.Value - steps[i-1].Value
			pos := value - steps[i-1].Value
			rat := pos / ran
			c1 := steps[i-1].Color
			c2 := step.Color
			c = models.Vector3F{
				X: (c1.X * (1.0 - rat)) + (c2.X * rat),
				Y: (c1.Y * (1.0 - rat)) + (c2.Y * rat),
				Z: (c1.Z * (1.0 - rat)) + (c2.Z * rat),
			}
			return c
		}
	}

	return c
}
