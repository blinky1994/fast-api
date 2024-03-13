from pydantic import BaseModel, Field
    
class PostBase(BaseModel):
    title: str
    content:  str
    published: bool = True
    

class PostCreate(PostBase):
    pass

