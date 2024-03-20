import humps
import typing as typ
from pydantic import BaseModel


#
# Base Models
#


class BaseCamelModel(BaseModel):
    class Config:
        alias_generator = humps.camelize
        populate_by_name = True
        extra = "ignore"


#
# Pagination Models
#


class PaginationParams(BaseCamelModel):
    limit: typ.Optional[int] = None
    offset: typ.Optional[int] = None


#
# Core Models
#


class Profile(BaseCamelModel):
    username: str
    following: bool
    bio: typ.Optional[str]
    image: typ.Optional[str]


class Comment(BaseCamelModel):
    id: str
    created_at: str
    updated_at: str
    body: str
    author: Profile


class User(BaseCamelModel):
    email: str
    # token: str
    username: str
    password: str
    bio: typ.Optional[str]
    image: typ.Optional[str]  # str or link


class Article(BaseCamelModel):
    slug: str
    title: str
    description: str
    body: str
    # tag_list: list[str]
    created_at: str
    updated_at: str
    # favorited: bool
    # favorites_count: int
    # author: Profile
