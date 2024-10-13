from sqlmodel import SQLModel, Field





class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session_id: str = Field(nullable=False)
    subtasks_total: int = Field(nullable=False)
    subtasks_completed: int = Field(nullable=False)
    completed: bool = Field(default=False)
    failure: str | None = Field(nullable=True)