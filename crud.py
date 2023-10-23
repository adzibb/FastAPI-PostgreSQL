from sqlalchemy.orm import Session
import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db:Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return  db.query(models.Todo).offset(skip).limit(limit).all()


def create_user_todo(db: Session, item: schemas.TodoCreate, user_id: int):
    db_item = models.Todo(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# =====================================================
def get_user_todo(db: Session, user_id: int, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id and models.Todo.owner_id == user_id).first()

def get_user_todo_by_title(db: Session, user_id: int, title: str):
    return db.query(models.Todo).filter(models.Todo.title == title and models.Todo.owner_id == user_id).first()


def get_user_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).filter(models.Todo.owner_id==user_id).all()


def remove_user_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    