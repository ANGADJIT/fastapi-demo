from json import load, dump

class PostsManager:
    def __init__(self) -> None:
        with open('../assets/json/posts.json') as _posts_data_file:
            self.__posts: list = load(_posts_data_file)

    def create_post(self, title: str, content: str, published: bool = True, rating: int = None) -> int:
        id: int = len(self.__posts) + 1

        self.__posts.append({
            'id': len(self.__posts) + 1,
            'title': title,
            'content': content,
            'published': published,
            'rating': rating
        })

        return id

    def get_all_posts(self) -> list:
        return self.__posts

    def get_post(self, id: int) -> dict:
        if id <= len(self.__posts):
            return self.__posts[id - 1]
        else:
            return None

    def get_latest_post(self) -> dict:
        return self.__posts[-1]

    def delete_post(self, id: int):
        if id <= len(self.__posts):
            self.__posts.pop(id - 1)
            return 'success'
        else:
            return None

    def update_post(self, id: int, new_post: dict):

        if id > len(self.__posts):
            return None

        new_post['id'] = id
        self.__posts[id - 1] = new_post
        return 'success'

    def __del__(self):
        with open('../assets/json/posts.json', 'w') as _posts_data_file:
            dump(self.__posts, _posts_data_file)
