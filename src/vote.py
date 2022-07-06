from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from schemas import Vote
import oauth2
from sqlalchemy.orm import Session
from schemas import VotesResponse
from vote_manager import VoteManager
from init_session import session_local

vote_manager: VoteManager = VoteManager(session_local=session_local)

router = APIRouter(
    prefix='/vote',
    tags=['Votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(vote_manager.get_db), current_user: int = Depends(oauth2.get_current_user)):
    result: VoteManager.VoteEnum = vote_manager.vote_post(
        vote=vote, db=db, user_id=int(current_user.id))

    if result == VoteManager.VoteEnum.VOTE_DOES_NOT_EXITS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'vote does not exits'})

    elif result == VoteManager.VoteEnum.VOTE_EXITS:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                            'message': 'post already voted'})

    elif result == VoteManager.VoteEnum.VOTED_UP:
        return {'message': 'post voted up'}

    return {'message': 'post voted down'}


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=VotesResponse)
def get_votes(post_id: int, db: Session = Depends(vote_manager.get_db), current_user: int = Depends(oauth2.get_current_user)):
    result = vote_manager.get_votes(db=db, post_id=post_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'vote does not exists'})

    return result