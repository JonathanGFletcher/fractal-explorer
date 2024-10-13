from models.fractal import (
    FractalConfig,
    RequestVideo,
)
from render.fractal import (
    fractal_image,
    render_julia,
)

from fastapi.routing import APIRouter
from pydantic import BaseModel

from typing import Optional, List





router = APIRouter()



@router.post("/image/julia")
async def image_julia(config: FractalConfig):
    pass


@router.post("/video/julia")
async def video_julia(config: RequestVideo):
    image = fractal_image(render_julia(config.start))
    image.save("/media/image.jpg")