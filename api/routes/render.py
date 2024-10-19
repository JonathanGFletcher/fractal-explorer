from database.sqlite import Session
from database.task import Task
from models.fractal import (
    Vector2F,
    JuliaConfig,
    MandelbrotConfig,
    JuliaVideoConfig,
    MandelbrotVideoConfig,
    julia_filename,
    mandelbrot_filename,
)
from render.fractal import (
    fractal_image,
    render_julia,
    render_mandelbrot,
)
from render.color import default_colors

from fastapi import BackgroundTasks, HTTPException
from fastapi.routing import APIRouter
import numpy as np
from cv2 import VideoWriter, cvtColor, COLOR_RGB2BGR

import os
import uuid
from typing import List





router = APIRouter()



# Image

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



# Video

def process_video_julia(id: str, path: str, video_width: int, video_height: int, frames: List[JuliaConfig]):
    try:
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
            with Session() as session:
                task = session.query(Task).filter(Task.session_id == id).first()
                task.subtasks_completed = i + 1
                session.add(task)
                session.commit()
            
        with Session() as session:
            task = session.query(Task).filter(Task.session_id == id).first()
            task.completed = True
            session.add(task)
            session.commit()
        video.release()
    except Exception as e:
        with Session() as session:
            task = session.query(Task).filter(Task.session_id == id).first()
            task.failure = str(e)
            session.add(task)
            session.commit()


@router.post("/video/julia")
async def new_video_julia(config: JuliaVideoConfig, background_tasks: BackgroundTasks):
    if not config.start.colors:
        config.start.colors = default_colors()
    id = str(uuid.uuid4())
    filename = f"{id}.avi"
    path = f"/media/{filename}"

    def linear_value(start: float, end: float, ratio: float) -> float:
        total_range = end - start
        return start + total_range * ratio
    
    def curve_value(start: float, end: float, scale: float):
        total_range = end - start
        progress = 1 - (1 / scale)
        return start + progress * total_range

    frames = []
    num_frames = config.seconds * 30
    for i in range(num_frames + 1):
        ratio = i / num_frames
        constant = Vector2F(
            x=linear_value(config.start.constant.x, config.end.constant.x, ratio),
            y=linear_value(config.start.constant.y, config.end.constant.y, ratio),
        )
        scale = np.pow(2, linear_value(np.log2(config.start.scale), np.log2(config.end.scale), ratio))
        center = Vector2F(
            x=curve_value(config.start.center.x, config.end.center.x, scale),
            y=curve_value(config.start.center.y, config.end.center.y, scale),
        )

        iterations = int(linear_value(config.start.iterations, config.end.iterations, ratio))
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
    
    task = Task(
        session_id=id,
        subtasks_total=len(frames),
        subtasks_completed=0,
        completed=False,
        failure=None,
    )
    with Session() as session:
        session.add(task)
        session.commit()

    video_width = config.start.dimensions.view_max_x - config.start.dimensions.view_min_x
    video_height = config.start.dimensions.view_max_y - config.start.dimensions.view_min_y

    background_tasks.add_task(
        process_video_julia, 
        id=id,
        path=path, 
        video_width=video_width, 
        video_height=video_height, 
        frames=frames
    )
    return { "id": id }


@router.get("/video/julia")
async def status_video_julia(id: str | None = None):
    if not id:
        raise HTTPException(status_code=400, detail="Session ID not provided")
    with Session() as session:
        task = session.query(Task).filter(Task.session_id == id).first()
    return task.json()