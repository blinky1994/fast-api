from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, models
from typing import List
from .. import oauth2

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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
      
@router.get('/latest')
def get_latest_post():
    return 'todo'

def raise404Exception(id: int):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')

@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise404Exception(id)
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    if post == None:
        raise404Exception(id)
        
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return { 'message': f'post with id: {id} has been deleted'}
        
@router.put('/{id}')
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_dict = post.model_dump(exclude_unset=True)
    post = post_query.first()
    
    if post == None:
        raise404Exception(id)
        
    post_query.update(post_dict, synchronize_session=False)
    db.commit()
    
    return post_query.first()