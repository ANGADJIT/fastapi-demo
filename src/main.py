from fastapi import FastAPI
import posts
import users
import auth
import vote
from fastapi.middleware.cors import CORSMiddleware

# ** EXAMPLE IMPORTS **
# from post_manager_sql import PostsManager #* PostsManager for [SQL] testing type
# from posts_manager_json import PostsManager #* PostsManager for [JSON] testing type

api = FastAPI()

# ** NETWORK SETTINGS **

origins: list[str] = ['*']

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@api.get('/')
def root():
    return {
        'about': 'This is a mock api which shows how real social media api\'s work'
    }


api.include_router(posts.router)
api.include_router(users.router)
api.include_router(auth.router)
api.include_router(vote.router)

# @api.on_event('startup') #* required only with [SQL] and [JSON] PostsManager class
# def startup():
#     pass

# @api.on_event('shutdown') #* required only with [SQL] and [JSON] PostsManager class
# def shutdown():
#     global posts_manager
#     del posts_manager
