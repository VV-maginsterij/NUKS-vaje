from typing import Union

from fastapi import FastAPI,HTTPException, status

from database import engine, Base, ToDo
import schemas
from sqlalchemy.orm import Session

from fastapi_versioning import VersionedFastAPI, version

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
@version(1)
def read_root():
    return "TODO app"


@app.post("/add", status_code = status.HTTP_201_CREATED)
@version(2)
def add_todo(todo: schemas.ToDo):

    session = Session(bind=engine, expire_on_commit=False)
    todoDB = ToDo(task = todo.task)
    session.add(todoDB)
    session.commit()
    id = todoDB.id
    session.close()
    return "Created new TODO item with id {id}"

@app.delete("/delete/{id}")
@version(2)
def delete_todo(id:int):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(ToDo).get(id)

    if todo:
        session.delete(todo)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="ToDo item with id {id} doesn't exist.")  
    session.close()
    return "Delete TODO"

@app.put("/update/{id}")
@version(2)
def update_todo(id: int, task: str):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(ToDo).get(id)
    if todo:
        todo.task = task #todo[field] = task -> da lahko preko apija določimo, katero polje posodabljamo
        session.commit()
    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail="ToDo item with id {id} doesn't exist.")
    return "Update TODO"

@app.get("/get/{id}")
@version(2)
def get_todo(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(ToDo).get(id)
    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail="ToDo item with id {id} doesn't exist.")
    return todo

@app.get("/list")
@version(2)
def get_all_todos():
    session = Session(bind=engine, expire_on_commit=False)
    todoall = session.query(ToDo).all()
    session.close()

    return todoall


app = VersionedFastAPI(app, version_format='{major}', prefix_format="/v{major}")