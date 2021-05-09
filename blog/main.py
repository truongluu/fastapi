from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Depends, Response, status, HTTPException
from .database import Base, engine, SessionLocal,get_db
from . import schemas, models, hashing
from sqlalchemy.orm import Session

# router
from .routers import blog,user,authentication

app = FastAPI()
app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)

Base.metadata.create_all(engine)