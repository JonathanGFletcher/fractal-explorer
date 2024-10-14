from constants.app import SQLITE_DB_URL
from models.fractal import (
    Vector2F,
    JuliaConfig,
    MandelbrotConfig,
    JuliaVideoConfig,
    MandelbrotVideoConfig,
    julia_filename,
    mandelbrot_filename,
)
# from models.task import Task
from render.fractal import (
    fractal_image,
    render_julia,
    render_mandelbrot,
)
from render.color import default_colors

from fastapi.routing import APIRouter
import numpy as np
from cv2 import VideoWriter, cvtColor, resize, COLOR_RGB2BGR

import os
import uuid





router = APIRouter()



@router.post("/image/julia")
async def image_julia(config: JuliaConfig):
    config.colors = default_colors()
    filename = julia_filename(config, '', 'png')
    path = f"/media/{filename}"
    url = f"/api/static/{filename}"
    if os.path.isfile(path):
        return { "url": url }

    image = fractal_image(render_julia(config))
    image.save(path)
    return { "url": url }


@router.post("/image/mandelbrot")
async def image_mandelbrot(config: MandelbrotConfig):
    config.colors = default_colors()
    filename = mandelbrot_filename(config, '', 'png')
    path = f"/media/{filename}"
    url = f"/api/static/{filename}"
    if os.path.isfile(path):
        return { "url": url }
    
    image = fractal_image(render_mandelbrot(config))
    image.save(path)
    return { "url": url }


@router.post("/video/julia")
async def video_julia(config: JuliaVideoConfig):
    if not config.start.colors:
        config.start.colors = default_colors()
    id = str(uuid.uuid4())
    filename = f"{id}.avi"
    path = f"/media/{filename}"

    def progress_value(start: float, end: float, ratio: float) -> float:
        return start + ((end - start) * ratio)

    frames = []
    num_frames = config.seconds * 30
    for i in range(num_frames + 1):
        ratio = i / num_frames
        constant = Vector2F(
            x=progress_value(config.start.constant.x, config.end.constant.x, ratio),
            y=progress_value(config.start.constant.y, config.end.constant.y, ratio),
        )
        center = Vector2F(
            x=progress_value(config.start.center.x, config.end.center.x, ratio),
            y=progress_value(config.start.center.y, config.end.center.y, ratio),
        )
        scale = np.pow(2, progress_value(np.log2(config.start.scale), np.log2(config.end.scale), ratio))
        iterations = int(progress_value(config.start.iterations, config.end.iterations, ratio))
        r = JuliaConfig(
            power=config.start.power,
            constant=constant,
            center=center,
            scale=scale,
            iterations=iterations,
            samples=config.start.samples,
            dimensions=config.start.dimensions,
            colors=config.start.colors,
        )
        frames.append(r)
    
    # task = Task(
    #     session_id=id,
    #     subtasks_total=len(frames),
    #     subtasks_completed=0,
    #     completed=False,
    #     failure=None,
    # )
    # engine = create_engine(SQLITE_DB_URL, connect_args={ "check_same_thread": False })

    video_width = config.start.dimensions.view_max_x - config.start.dimensions.view_min_x
    video_height = config.start.dimensions.view_max_y - config.start.dimensions.view_min_y
    video = VideoWriter(
        path, 
        VideoWriter.fourcc(*'MJPG'), 
        30, 
        (video_width, video_height),
        isColor=True,
    )

    for i, frame_conf in enumerate(frames):
        frame_data = render_julia(frame_conf)
        frame = cvtColor(frame_data, COLOR_RGB2BGR)
        video.write(frame)
        print(f"Video: {id}: Rendered {i+1} / {len(frames)} frames")
    print(f"Video {id}: Rendering complete")
    video.release()