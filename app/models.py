from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN
from .database import Base

class Post(Base): 
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(VARCHAR, nullable=False)
    content = Column(VARCHAR, nullable=False)
    published = Column(BOOLEAN, default=False)
    
    