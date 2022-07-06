from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas import Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from init_session import session_local
from auth_manager import AuthManager

router = APIRouter(tags=['Authentication'])

auth_manager = AuthManager(session_local)


@router.post('/login',response_model=Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth_manager.get_db)):
    result = auth_manager.login(credentials=credentials, db=db)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentails')

    elif result != False:
        return {'access_token': result, 'token_type': 'bearer'}

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentails')
