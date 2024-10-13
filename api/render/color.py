from models.fractal import ColorStep, Vector3F

from typing import List


def default_colors() -> List[ColorStep]:
	steps = []
	steps.append(ColorStep(value=0.0, color=Vector3F(x=17.0, y=3.0, z=77.0)))
	steps.append(ColorStep(value=0.03, color=Vector3F(x=38.0, y=15.0, z=141.0)))
	steps.append(ColorStep(value=0.05, color=Vector3F(x=111.0, y=45.0, z=12.0)))
	steps.append(ColorStep(value=0.25, color=Vector3F(x=203.0, y=52.0, z=82.0)))
	steps.append(ColorStep(value=0.5, color=Vector3F(x=250.0, y=102.0, z=34.0)))
	steps.append(ColorStep(value=0.85, color=Vector3F(x=254.0, y=221.0, z=8.0)))
	steps.append(ColorStep(value=0.95, color=Vector3F(x=101.0, y=240.0, z=142.0)))
	steps.append(ColorStep(value=1.0, color=Vector3F(x=255.0, y=255.0, z=255.0)))

	return steps
