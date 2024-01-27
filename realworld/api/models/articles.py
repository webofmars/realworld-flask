import typing as typ
from pydantic import model_serializer
from realworld.api.core.models import BaseCamelModel, Article, Comment, PaginationParams

#
# Data Definitions
#


class CreateArticleData(BaseCamelModel):
    title: str
    description: str
    body: str
    tag_list: typ.Optional[str]


class UpdateArticleData(BaseCamelModel):
    # Note: `slug` gets updated when title is changed
    title: typ.Optional[str]
    description: typ.Optional[str]
    body: typ.Optional[str]
    tag_list: typ.Optional[str]


class CreateCommentData(BaseCamelModel):
    body: str


#
# Request Models
#


# --- Query Params ---
class GetArticlesQueryParams(PaginationParams):
    tag: typ.Optional[str] = None
    author: typ.Optional[str] = None
    favorited: typ.Optional[bool] = None


class GetFeedQueryParams(PaginationParams):
    pass


# --- Post Body ---
class CreateArticleRequest(BaseCamelModel):
    article: CreateArticleData


class UpdateArticleRequest(BaseCamelModel):
    article: UpdateArticleData


class CreateCommentRequest(BaseCamelModel):
    comment: CreateCommentData


#
# Response Models
#


class SingleArticleResponse(BaseCamelModel):
    article: Article


class MultipleArticlesResponse(BaseCamelModel):
    articles: list[Article]


class DeleteArticleResponse(BaseCamelModel):
    slug: str

    @model_serializer
    def ser_model(self) -> dict:
        return {"message": f"Article `{self.slug}` successfully deleted."}


class SingleCommentResponse(BaseCamelModel):
    comment: Comment


class ArticleCommentsResponse(BaseCamelModel):
    comments: list[Comment]


class DeleteCommentResponse(BaseCamelModel):
    id: str
    slug: str

    @model_serializer
    def ser_model(self) -> dict:
        return {
            "message": f"Comment {self.id} from Article `{self.slug}` successfully deleted."
        }
