from pydantic import BaseModel, Field
from datetime import datetime    

class PostBase(BaseModel):
    title: str
    content:  str
    published: bool = True
    
    
class PostCreate(PostBase):
    pass

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime