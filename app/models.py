from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN, TIMESTAMP
from .database import Base
from datetime import datetime

class Post(Base): 
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(VARCHAR, nullable=False)
    content = Column(VARCHAR, nullable=False)
    published = Column(BOOLEAN, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    