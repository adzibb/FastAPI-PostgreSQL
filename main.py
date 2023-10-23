from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db, user=user)


@app.get('/users/', response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.post('/users/{user_id}/todos/', response_model=schemas.Todo)
def create_item_for_user(
        user_id: int, item: schemas.TodoCreate, db: Session = Depends(get_db)
):
    return crud.create_user_todo(db=db, item=item, user_id=user_id)


@app.get('/todos/', response_model=list[schemas.Todo])
def read_items(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


# =========================================================================
@app.get('/todos/{user_id}/', response_model=list[schemas.Todo])
def read_user_todos(user_id: int, skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    user_todos = crud.get_user_todos(db=db, user_id=user_id, skip=skip, limit=limit)
    return user_todos


@app.get('/todo/{user_id}/{todo_id}', response_model=schemas.Todo)
def read_todo_by_id(user_id: int, todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_user_todo(db=db, user_id=user_id, todo_id=todo_id)
    return todo


@app.get('/todo/{user_id}/', response_model=schemas.Todo)
def read_todo_by_title(user_id: int, title: str, db: Session = Depends(get_db)):
    todo = crud.get_user_todo_by_title(db=db, user_id=user_id, title=title)
    return todo


@app.delete('/todo/{todo_id}/', response_model=schemas.Todo)
def remove_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.remove_user_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Todo with ID {todo_id} not found')
    db.delete(todo)
    db.commit()
    return todo


