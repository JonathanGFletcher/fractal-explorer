from pydantic import BaseModel
import numpy as np

from typing import Optional, List





class Vector2F(BaseModel):
    x: float
    y: float


class Vector3F(BaseModel):
    x: float
    y: float
    z: float


class ColorStep(BaseModel):
    value: float
    color: Vector3F


class FractalDimensions(BaseModel):
    width: int
    height: int
    view_min_x: int
    view_min_y: int
    view_max_x: int
    view_max_y: int


class FractalConfig(BaseModel):
    power: int
    constant: Vector2F
    center: Vector2F
    scale: float
    iterations: int
    samples: int
    dimensions: FractalDimensions
    colors: Optional[List[ColorStep]]

class RequestVideo(BaseModel):
    start: FractalConfig
    end: FractalConfig
    seconds: int


def julia_filename(r: FractalConfig, prefix: str, extension: str) -> str:
	if prefix != "":
		prefix += "_"
          
	return "{0}p{1}_kx{2}_ky{3}_cx{4}_cy{5}_sc{6}_it{7}_sa{8}_dw{9}_dh{10}_dmix{11}_dmiy{12}_dmax{13}_dmay{14}.{15}".format(prefix, r.power, r.constant.x, r.constant.y, r.center.x, r.center.y, r.scale, r.iterations, r.samples, r.dimensions.width, r.dimensions.height, r.dimensions.view_min_x, r.dimensions.view_min_y, r.dimensions.view_max_x, r.dimensions.view_max_y, extension)