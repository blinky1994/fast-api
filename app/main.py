from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)        
app.include_router(user.router)        
app.include_router(post.router)        

@app.get('/')
def default():
    return {'message':'Hello World'}

