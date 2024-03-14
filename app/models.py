from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, TIMESTAMP, String, text
from .database import Base
from datetime import datetime

class Post(Base): 
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(VARCHAR, nullable=False)
    content = Column(VARCHAR, nullable=False)
    published = Column(BOOLEAN, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(), server_default=text('now()'), nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(), server_default=text('now()'), nullable=False)
    