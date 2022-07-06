from typing import Optional
from pydantic import BaseModel, EmailStr


class Posts(BaseModel):  # base class for posts
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    user_id: int


class PostCreate(Posts):
    pass


class UserCreateResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class PostResponse(Posts):
    id: int
    rating: int = None
    onwer: UserCreateResponse

    class Config:
        orm_mode = True

# for user


class Users(BaseModel):
    email: EmailStr
    password: str


class UserCreate(Users):
    pass


class UserGetResponse(UserCreateResponse):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

# for votes


class Vote(BaseModel):
    post_id: int
    dir: bool


class VotesResponse(Posts):
    votes: int
