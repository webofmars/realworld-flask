import typing as typ
from realworld.api.core.models import BaseCamelModel, Article, Comment


# GET /api/articles
# GET /api/articles/feed


# POST /api/articles
class CreateArticleData(BaseCamelModel):
    title: str
    description: str
    body: str
    tag_list: typ.Optional[str] = None


class CreateArticleRequest(BaseCamelModel):
    article: CreateArticleData


# PUT /api/articles/:slug
class UpdateArticleData(BaseCamelModel):
    title: typ.Optional[str]
    description: typ.Optional[str]
    body: typ.Optional[str]


class UpdateArticleRequest(BaseCamelModel):
    article: UpdateArticleData


# POST /api/articles/:slug/comments
class CreateCommentData(BaseCamelModel):
    body: str


class CreateCommentRequest(BaseCamelModel):
    comment: CreateCommentData


class CreateCommentResponse(BaseCamelModel):
    comment: Comment


#
# Shared Response Models
#
class SingleArticleResponse(BaseCamelModel):
    article: Article


class MultipleArticlesResponse(BaseCamelModel):
    articles: typ.List[Article]


class MultipleCommentsResponse(BaseCamelModel):
    comments: typ.List[Comment]


# GET /api/tags
class GetTagsResponse(BaseCamelModel):
    tags: list[str]