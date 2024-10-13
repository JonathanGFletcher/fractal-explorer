from models.fractal import (
    FractalConfig,
    RequestVideo,
    julia_filename,
)
from render.fractal import (
    fractal_image,
    render_julia,
)
from render.color import default_colors

from fastapi.routing import APIRouter
from pydantic import BaseModel

import os
from typing import Optional, List





router = APIRouter()



@router.post("/image/julia")
async def image_julia(config: FractalConfig):
    config.colors = default_colors()
    filename = julia_filename(config, '', 'png')
    path = f"/media/{filename}"
    url = f"/api/static/{filename}"
    if os.path.isfile(path):
        return { "url": url }

    image = fractal_image(render_julia(config))
    image.save(path)
    return { "url": url }



@router.post("/video/julia")
async def video_julia(config: RequestVideo):
    config.start.colors = default_colors()