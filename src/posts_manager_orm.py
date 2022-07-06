from sqlalchemy.orm import Session
from models import Post


class PostsManager:

    def __init__(self, session_local) -> None:
        self.session_local = session_local

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        except:
            db.close()

    def get_all_posts(self, db: Session, limit: int, skip: int, search: str) -> list:
        return db.query(Post).filter(Post.title.contains(search)).limit(limit).offset(skip).all()

    def create_post(self, new_post: dict, current_user_id: int, db: Session) -> int:
        post: Post = Post(**new_post)

        if current_user_id == post.user_id:
            try:
                db.add(post)
                db.commit()

            except:
                return None

            return post.id

        else:
            return -1

    def get_post(self, db: Session, id: int) -> int:
        return db.query(Post).filter(Post.id == id).first()

    def delete_post(self, id: int, user_id: int, db: Session):
        post = db.query(Post).filter(Post.id == id)

        if not post.first():
            return None

        post_user_id = post.first().user_id

        if post_user_id == user_id:
            post.delete(synchronize_session=False)
            db.commit()

            return user_id

        return -1

    def update_post(self, db: Session, id: int, new_post: dict):
        post = db.query(Post).filter(Post.id == id)

        if not post.first():
            return None

        try:
            post.update(new_post, synchronize_session=False)
            db.commit()
        except(Exception):
            return -1

        return 'success'
