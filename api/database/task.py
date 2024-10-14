from database.sqlite import Base
from sqlalchemy import (
    Column, Integer, String, Boolean
)





class Task(Base):
    __tablename__ = "tasks"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    session_id = Column("session_id", String, nullable=False)
    subtasks_total = Column("subtasks_total", Integer, nullable=False)
    subtasks_completed = Column("subtasks_completed", Integer, nullable=False, default=0)
    completed = Column("completed", Boolean, nullable=False, default=False)
    failure = Column("failure", String, nullable=True)

    def __init__(self, session_id, subtasks_total, subtasks_completed, completed, failure):
        self.session_id = session_id
        self.subtasks_total = subtasks_total
        self.subtasks_completed = subtasks_completed
        self.completed = completed
        self.failure = failure

    def __repr__(self):
        return f"{self.id} ({self.session_id}) Progress: {self.subtasks_completed / self.subtasks_total} Completed: {self.completed} Failure: {self.failure}"
    
    def json(self):
        return {
            "session_id": self.session_id,
            "subtasks_total": self.subtasks_total,
            "subtasks_completed": self.subtasks_completed,
            "completed": self.completed,
            "failure": self.failure,
        }