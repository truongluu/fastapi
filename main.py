from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Depends, Response, status
from database import Base, engine, SessionLocal
from schemas import Blog as BlogSchema
from sqlalchemy.orm import Session
from models import Blog

app = FastAPI()

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def all(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/blog")
def create(request: BlogSchema, db: Session =  Depends(get_db)):
    new_blog = Blog(title=request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog/{id}")
def get(id, response: Response, db:Session = Depends(get_db)):
    blog  = db.query(Blog).filter(Blog.id == id).first()
    if blog is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": f"Blog with the id {id} is not available"}
    return blog