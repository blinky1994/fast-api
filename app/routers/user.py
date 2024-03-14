from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import hash

router = APIRouter()

@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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

@router.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exist')
    
    return user