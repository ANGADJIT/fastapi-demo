from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
import oauth2
import schemas
from init_session import session_local
from posts_manager_orm import PostsManager

router = APIRouter(prefix='/posts', tags=['Posts'])
posts_manager = PostsManager(session_local=session_local)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_post(posts: schemas.PostCreate, db: Session = Depends(posts_manager.get_db), user_id: int = Depends(oauth2.get_current_user)):
    id: int = posts_manager.create_post(
        db=db, new_post=posts.dict(), current_user_id=int(user_id.id))

    if not id:

        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail={
            'error': f'failed to create post: no user found with id {user_id.id}'
        })

    if id == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'error': 'can\'t perform the requested operation'})

    return {
        'status': f'posts created successfully 😎 with id : {id}'
    }


@router.get('/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(posts_manager.get_db), user_id: int = Depends(oauth2.get_current_user)):
    data = posts_manager.get_post(id=id, db=db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no post found with id {id} 🙄')

    return data


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(posts_manager.get_db), user_id: int = Depends(oauth2.get_current_user)):
    data = posts_manager.delete_post(id=id, user_id=int(user_id.id), db=db)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no post found with id {id} 🙄')

    if data == -1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
            'error': 'can\'t perform requested operation'
        })

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_post(id: int, post: schemas.Posts, db: Session = Depends(posts_manager.get_db), user_id: int = Depends(oauth2.get_current_user)):
    data = posts_manager.update_post(id=id, new_post=post.dict(), db=db)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'no post found with id {id} 🙄'})

    if data == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': f'no user found with id {post.user_id} 🙄'})

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/', response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(posts_manager.get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] = ''):
    return posts_manager.get_all_posts(db=db, limit=limit, skip=skip, search=search)
