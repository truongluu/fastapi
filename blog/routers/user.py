from fastapi import Depends, APIRouter, status, HTTPException, Response
from ..database import get_db
from .. import schemas, models
from sqlalchemy.orm import Session

router = APIRouter(tags=["users"], prefix='/user')

@router.post('/')
def create_user(request:schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password= hashing.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@router.get("/{id}", response_model=schemas.ShowUser)
def get(id, response: Response, db:Session = Depends(get_db)):
    user  = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with the id {id} is not available")
    return user