from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..utils import verify
from .. import oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    print(verify(user_credentials.password, existing_user.password))
    if not verify(user_credentials.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    access_token = oauth2.create_access_token(data={'id': existing_user.id})
    
    return {'access_token': access_token, 'token_type': 'bearer'}