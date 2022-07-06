from schemas import UserGetResponse, UserCreateResponse, UserCreate
from users_manager_orm import UsersManager
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from init_session import session_local

router = APIRouter(prefix='/users',tags=['Users'])
users_manager = UsersManager(session_local=session_local)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def create_user(user: UserCreate, db: Session = Depends(users_manager.get_db)):
    response = users_manager.create_user(db=db, user=user.dict())

    if not response:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail='email already in use')

    return response


@router.get('/{id}', response_model=UserGetResponse)
def get_user(id: int, db: Session = Depends(users_manager.get_db)):
    user = users_manager.get_user(db=db, id=id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} not found')

    return user

