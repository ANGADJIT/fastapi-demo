from itertools import count
import mysql.connector as connector


class PostsManager:
    def __init__(self) -> None:
        try:
            self.__postsDb = connector.connect(
                host='localhost',
                user='root',
                password='angad1234',
                database='fastapi'
            )

            self.__cursor = self.__postsDb.cursor()

        except(Exception) as e:
            print(e)
            exit()

    def __to_dict(self, post: tuple) -> dict:
        return {
            'id': post[0],
            'title': post[1],
            'content': post[2],
            'published': bool(post[3]),
            'rating': post[4]
        }

    def create_post(self, title: str, content: str, published: bool = True, rating: int = None) -> int:
        if rating is None:
            rating = 'NULL'

        self.__cursor.execute(
            f"INSERT INTO posts (`Title`,`Content`,`Published`,`Rating`) VALUES('{title}','{content}',{published},{rating})")
        self.__postsDb.commit()

        self.__cursor.execute('SELECT COUNT(*) from posts')
        count = self.__cursor.fetchall()[0][0]
        self.__posts_count = count

        return count

    def get_all_posts(self) -> list:
        parsed_posts: list[dict] = []
        self.__cursor.execute('SELECT * FROM posts')
        posts: list[tuple] = self.__cursor.fetchall()

        for post in posts:
            parsed_posts.append(self.__to_dict(post))

        return parsed_posts

    def get_post(self, id: int) -> dict:
        self.__cursor.execute(f'SELECT * FROM posts WHERE ID={id}')
        post: list[tuple] = self.__cursor.fetchall()

        if len(post) != 0:
            return post[0]

        return None

    def delete_post(self, id: int):
        self.__cursor.execute('SELECT COUNT(*) FROM posts')
        prev_count: int = self.__cursor.fetchall()[0][0]

        self.__cursor.execute(f'DELETE FROM posts WHERE ID={id}')

        self.__cursor.execute('SELECT COUNT(*) FROM posts')
        new_count: int = self.__cursor.fetchall()[0][0]

        if prev_count != new_count:
            self.__postsDb.commit()
            return 'success'

        return None

    def update_post(self, id: int, new_post: dict):
        if self.get_post(id) is not None:
            if new_post.get('rating') is None:
                new_post['rating'] = 'NULL'

            self.__cursor.execute(
                f"UPDATE posts SET Title='{new_post['title']}',Content='{new_post['content']}',Published={int(new_post['published'])},Rating={new_post['rating']} WHERE Id={id}")
            self.__postsDb.commit()

            return 'success'

        return None

    def __del__(self):
        self.__cursor.close()
        self.__postsDb.close()

