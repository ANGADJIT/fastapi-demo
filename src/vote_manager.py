from select import select
from unittest import result
from schemas import Vote
from models import Votes, Post
import enum
from sqlalchemy import func
from sqlalchemy.orm import Session


class VoteManager:

    class VoteEnum(enum.Enum):  # this represents constants for VOTES
        VOTED_UP = 1
        VOTED_DOWN = 2
        VOTE_EXITS = 3
        VOTE_DOES_NOT_EXITS = 4

    def __init__(self, session_local) -> None:
        self.session_local = session_local

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        except:
            db.close()

    def vote_post(self, vote: Vote, db: Session, user_id: int) -> VoteEnum:
        query = db.query(Votes).filter(
            Votes.post_id == vote.post_id, user_id == Votes.user_id)
        found_check = query.first()

        if vote.dir:
            if found_check:
                return self.VoteEnum.VOTE_EXITS

            try:
                new_vote = Votes(post_id=vote.post_id, user_id=user_id)
                db.add(new_vote)
                db.commit()

                return self.VoteEnum.VOTED_UP

            except(Exception):
                return self.VoteEnum.VOTE_DOES_NOT_EXITS

        else:
            if found_check:
                query.delete(synchronize_session=False)
                db.commit()

                return self.VoteEnum.VOTED_DOWN

            return self.VoteEnum.VOTE_DOES_NOT_EXITS

    def get_votes(self, db: Session, post_id: int):
        result = db.execute(
            f'SELECT posts.*, COUNT(votes.post_id) as votes FROM posts JOIN votes ON posts.id = votes.post_id WHERE votes.post_id = {post_id}')
        
        votes = result.first()

        if votes[0] is None:
            return None

        return votes
