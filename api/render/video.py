from models.fractal import VideoConfig, JuliaConfig, Vector2F
from database.task import Task
from database.sqlite import Session
from render.fractal import render

import numpy as np
from cv2 import VideoWriter, cvtColor, COLOR_RGB2BGR





def process_frames(config: VideoConfig, FrameType: ...) -> list:
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
        scale = np.pow(2, linear_value(np.log2(config.start.scale), np.log2(config.end.scale), ratio))
        center = Vector2F(
            x=curve_value(config.start.center.x, config.end.center.x, scale),
            y=curve_value(config.start.center.y, config.end.center.y, scale),
        )

        additional_config = {}
        if FrameType == JuliaConfig:
            additional_config["constant"] = Vector2F(
                x=linear_value(config.start.constant.x, config.end.constant.x, ratio),
                y=linear_value(config.start.constant.y, config.end.constant.y, ratio),
            )
            additional_config["power"] = config.start.power

        iterations = int(linear_value(config.start.iterations, config.end.iterations, ratio))
        r = FrameType(
            center=center,
            scale=scale,
            iterations=iterations,
            samples=config.start.samples,
            dimensions=config.start.dimensions,
            colors=config.start.colors,
            **additional_config,
        )
        frames.append(r)
    return frames


def process_video(id: str, path: str, video_width: int, video_height: int, frames: list, render_func: callable):
    try:
        video = VideoWriter(
            path, 
            VideoWriter.fourcc(*'MJPG'), 
            30, 
            (video_width, video_height),
            isColor=True,
        )

        for i, frame_conf in enumerate(frames):
            frame_data = render(frame_conf, render_func)
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