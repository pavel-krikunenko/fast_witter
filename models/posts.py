from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.base import SuccessResponse, ListData


class Post(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    author_id: int
    likes: Optional[list[int]] = []


class NewPost(BaseModel):
    title: str
    body: str


class UpdatePost(BaseModel):
    title: Optional[str]
    body: Optional[str]


class PostSuccessResponse(SuccessResponse):
    data: Post


class PostsListData(ListData):
    items: list[Post]


class PostsListSuccessResponse(SuccessResponse):
    data: PostsListData
