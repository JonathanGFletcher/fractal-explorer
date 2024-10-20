from database.sqlite import Session
from database.task import Task
from models.fractal import (
    JuliaConfig,
    MandelbrotConfig,
    JuliaVideoConfig,
    MandelbrotVideoConfig,
    julia_filename,
    mandelbrot_filename,
)
from render.fractal import (
    fractal_image,
    render,
    render_julia,
    render_mandelbrot,
)
from render.video import process_frames, process_video
from render.color import default_colors

from fastapi import BackgroundTasks, HTTPException
from fastapi.routing import APIRouter


import os
import uuid





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
    
    image = fractal_image(render(config, render_julia))
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
    
    image = fractal_image(render(config, render_mandelbrot))
    image.save(path)
    return { "url": url }



# Video

@router.get("/video/julia")
async def status_video_julia(id: str | None = None):
    if not id:
        raise HTTPException(status_code=400, detail="Session ID not provided")
    with Session() as session:
        task = session.query(Task).filter(Task.session_id == id).first()
    return task.json()

@router.post("/video/julia")
async def new_video_julia(config: JuliaVideoConfig, background_tasks: BackgroundTasks):
    if not config.start.colors:
        config.start.colors = default_colors()
    id = str(uuid.uuid4())
    filename = f"{id}.avi"
    path = f"/media/{filename}"

    frames = process_frames(config, JuliaConfig)
    
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
        process_video, 
        id=id,
        path=path, 
        video_width=video_width, 
        video_height=video_height, 
        frames=frames,
        render_func=render_julia,
    )
    return { "id": id }


@router.get("/video/mandelbrot")
async def status_video_mandelbrot(id: str | None = None):
    if not id:
        raise HTTPException(status_code=400, detail="Session ID not provided")
    with Session() as session:
        task = session.query(Task).filter(Task.session_id == id).first()
    return task.json()

@router.post("/video/mandelbrot")
async def new_video_mandelbrot(config: MandelbrotVideoConfig, background_tasks: BackgroundTasks):
    if not config.start.colors:
        config.start.colors = default_colors()
    id = str(uuid.uuid4())
    filename = f"{id}.avi"
    path = f"/media/{filename}"

    frames = process_frames(config, MandelbrotConfig)
    
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
        process_video, 
        id=id,
        path=path, 
        video_width=video_width, 
        video_height=video_height, 
        frames=frames,
        render_func=render_mandelbrot,
    )
    return { "id": id }