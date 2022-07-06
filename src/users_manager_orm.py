from models import Users
from sqlalchemy.orm import Session
from generic_methods import hash_password


class UsersManager:

    def __init__(self, session_local) -> None:
        self.session_local = session_local

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        except:
            db.close()

    def create_user(self, db: Session, user: dict) -> Users:
        user = Users(**user)
        user.password = hash_password(user.password)

        try:
            db.add(user)
            db.commit()

        except Exception:
            return None

        return user

    def get_user(self, db: Session, id: int) -> Users:
        user = db.query(Users).filter(Users.id == id)

        if not user.first():
            return None

        return user.first()
