from sqlalchemy.orm import Session
from oauth2 import create_access_token
from models import Users
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from generic_methods import verify


class AuthManager:

    def __init__(self, session_local) -> None:
        self.session_local = session_local

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        except:
            db.close()

    def login(self, db: Session, credentials: OAuth2PasswordRequestForm):
        user = db.query(Users).filter(Users.email == credentials.username)

        if not user.first():
            return None

        # if user is there then we have check for password 

        result = verify(user_password=credentials.password,
                        actual_password=user.first().password)

        if result:
            access_token = create_access_token(
                data={'user_id': user.first().id})
            
            return access_token

        else:
            return False
