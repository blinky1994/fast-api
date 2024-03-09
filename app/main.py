from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel): 
    id: Optional[int] = Field(default=None, readOnly=True, alias="_id")
    title: str
    content:  str
    published: bool = True

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

@app.get('/posts', status_code=status.HTTP_201_CREATED)
def get_posts():
    cursor.execute('select * from posts;')
    posts = cursor.fetchall()
    print(posts)
    return { 'data': posts }

@app.post('/createpost')
def create_post(post : Post):
    cursor.execute('insert into posts (title, content, published) values (%s, %s, %s) returning *', (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return { 
        'data' : new_post
    }

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

@app.get('/posts/{id}')
def get_post(id: int):
   cursor.execute('select * from posts where id = %s', (str(id),))
   post = cursor.fetchone()
   conn.commit()
   if not post:
    raise404Exception(id)
   return { 'post_detail': post }

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('delete from posts where id = %s returning *', (str(id),))
    deleted_post = cursor.fetchone()
    print(deleted_post)
    conn.commit()
    if not deleted_post:
        raise404Exception(id)
    return { 'message': f'post with id: {id} has been deleted'}
        
@app.put('/posts/{id}')
def delete_post(id: int, post: Post):
    cursor.execute('update posts set title = %s, content = %s, published = %s where id = %s returning *', (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    return { 'message': f'post with id: {id} has been updated', 'body': updated_post}
        
