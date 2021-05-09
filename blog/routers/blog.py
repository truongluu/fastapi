from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, token, oauth2

router = APIRouter(tags=["blogs"], prefix='/blog')

@router.get("/", response_model=List[schemas.Blog])
def all(db: Session = Depends(get_db), user: models.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/")
def create(request: schemas.Blog, db: Session =  Depends(get_db)):
    new_blog = models.Blog(title=request.title, body = request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/{id}", response_model=schemas.ShowBlog)
def get(id, response: Response, db:Session = Depends(get_db)):
    blog  = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Blog with the id {id} is not available")
    return blog

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    return 'done'
    

@router.put("/{id}")
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    print(request)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request)
    db.commit()
    return 'Updated'
