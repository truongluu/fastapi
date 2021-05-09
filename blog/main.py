from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Depends, Response, status, HTTPException
from .database import Base, engine, SessionLocal
from . import schemas, models, hashing
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs



@app.post("/blog")
def create(request: schemas.Blog, db: Session =  Depends(get_db)):
    new_blog = models.Blog(title=request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog/{id}", response_model=schemas.ShowBlog)
def get(id, response: Response, db:Session = Depends(get_db)):
    blog  = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Blog with the id {id} is not available")
    return blog

@app.delete("/blog/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    return 'done'
    

@app.put("/blog/{id}")
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    print(request)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request)
    db.commit()
    return 'Updated'

@app.post('/user')
def create_user(request:schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password= hashing.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@app.get("/user/{id}", response_model=schemas.ShowUser)
def get(id, response: Response, db:Session = Depends(get_db)):
    user  = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with the id {id} is not available")
    return user