from constants.app import (
    APP_NAME,
    LOGGER_FORMAT,
    SQLITE_DB_URL
)
from routes.render import router as render_router

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import create_engine, SQLModel

import sys
import logging





app = FastAPI(title=APP_NAME)
app.include_router(render_router, prefix="/render")
app.mount("/static", StaticFiles(directory="/media"), name="static")

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(LOGGER_FORMAT)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

# Database
engine = create_engine(SQLITE_DB_URL, connect_args={ "check_same_thread": False })
SQLModel.metadata.create_all(engine)
logger.info("Database initialized...")