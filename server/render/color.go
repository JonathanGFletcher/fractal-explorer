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

func DefaultColors() []models.ColorStep {
	steps := []models.ColorStep{}
	steps = append(steps, models.ColorStep{Value: 0.0, Color: models.Vector3F{X: 17.0 / 255.0, Y: 3.0 / 255.0, Z: 77.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.03, Color: models.Vector3F{X: 38.0 / 255.0, Y: 15.0 / 255.0, Z: 141.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.05, Color: models.Vector3F{X: 111.0 / 255.0, Y: 45.0 / 255.0, Z: 12.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.25, Color: models.Vector3F{X: 203.0 / 255.0, Y: 52.0 / 255.0, Z: 82.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.5, Color: models.Vector3F{X: 250.0 / 255.0, Y: 102.0 / 255.0, Z: 34.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.85, Color: models.Vector3F{X: 254.0 / 255.0, Y: 221.0 / 255.0, Z: 8.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 0.95, Color: models.Vector3F{X: 101.0 / 255.0, Y: 240.0 / 255.0, Z: 142.0 / 255.0}})
	steps = append(steps, models.ColorStep{Value: 1.0, Color: models.Vector3F{X: 1.0, Y: 1.0, Z: 1.0}})

	return steps
}
