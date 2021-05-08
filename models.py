from sqlalchemy import Column, String, Integer
from database import Base

class Blog(Base):
    __tablename__ ="blog"
    id = Column(Integer, primary_key=True, index= True)
    title = Column(String)
    body = Column(String)