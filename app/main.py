from random import randrange
from fastapi import Body, FastAPI, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import schemas
from typing import List
from .utils import hash


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
        

@app.get('/')
def default():
    return {'message':'Hello World'}

@app.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts

@app.post('/createpost', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_dict = post.model_dump()
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def find_post(id: int):
    for p in posts:
        if p['id'] == id:
            return p
        
def find_post_index(id: int):
    for i, p in enumerate(posts):
        if (p['id']) == id:
            return i
      
@app.get('/posts/latest')
def get_latest_post():
    return 'todo'

def raise404Exception(id: int):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')

@app.get('/posts/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise404Exception(id)
    return post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    if post == None:
        raise404Exception(id)
        
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return { 'message': f'post with id: {id} has been deleted'}
        
@app.put('/posts/{id}')
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_dict = post.model_dump(exclude_unset=True)
    post = post_query.first()
    
    if post == None:
        raise404Exception(id)
        
    post_query.update(post_dict, synchronize_session=False)
    db.commit()
    
    return post_query.first()
        
@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    
    user.password = hash(user.password)
    new_user = models.User(**user.model_dump())
    
    user_query = db.query(models.User).filter(models.User.email == user.email)

    if user_query.first() != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'There is an issue creating this user')
        
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exist')
    
    return user