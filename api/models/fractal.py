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