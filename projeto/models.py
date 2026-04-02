from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class TasksBlocks(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: Optional[str] = Field(default='Bloco de tarefas sem título')
  icon: Optional[str] = Field(default=None)
  cover: Optional[str] = Field(default=None)

  tasks: List["Tasks"] = Relationship(back_populates="tasksblocks")

class Tasks(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: Optional[str] = Field(default='Tarefa sem título')
  description: Optional[str] = Field(default='Tarefa sem descrição')
  completed: Optional[bool] = Field(default=False)
  block_id: int = Field(foreign_key="tasksblocks.id")

  tasksblocks: TasksBlocks | None = Relationship(back_populates="tasks")