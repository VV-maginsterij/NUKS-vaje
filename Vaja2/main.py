from typing import Union

from fastapi import FastAPI

from database import engine, Base, ToDo
import schemas
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def read_root():
    return "TODO app"


@app.post("/add")
def add_todo(todo: schemas.ToDo):

    session = Session(bind=engine, expire_on_commit=False)
    todoDB = ToDo(task = todo.task)
    session.add(todoDB)
    session.commit()
    id = todoDB.id
    session.close()
    return "Create new TODO item with id {id}"

@app.delete("/delete/{id}")
def delete_todo(id:int):
    return "Delete TODO"

@app.put("/update/{id}")
def update_todo(id: int):
    return "Update TODO"

@app.get("/get/{id}")
def get_todo(id: int):
    return "Get TODO"

@app.get("/list")
def get_all_todos():
    return "Get all TODOs"
