from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import user, post
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
        
while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful')
        break
    except Exception as error:
        print('Connecting to database failed')
        print(f'Error: {error}')
        time.sleep(2)

app.include_router(user.router)        
app.include_router(post.router)        

@app.get('/')
def default():
    return {'message':'Hello World'}

