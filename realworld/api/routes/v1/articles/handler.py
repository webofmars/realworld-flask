import typing as typ
from sqlalchemy.engine import Connection
from realworld.api.core.models import Article, Comment
from realworld.api.routes.v1.articles.models import (
    CreateArticleData,
    UpdateArticleData,
    CreateCommentData,
)

# from realworld.api.handlers.queries import get_articles_query
# from realworld.api.routes.v1.articles.models import MultipleArticlesResponse


def get_articles(
    db_conn: Connection,
    *,
    curr_user_id: typ.Optional[str] = None,
    tag_filter: typ.Optional[str] = None,
    author_username_filter: typ.Optional[str] = None,
    favorited_by_username_filter: typ.Optional[str] = None,
    limit: typ.Optional[int] = 20,
    offset: typ.Optional[int] = 0,
) -> typ.List[Article]: ...


def get_feed_articles(
    db_conn: Connection,
    curr_user_id: str,
    limit: typ.Optional[int] = 20,
    offset: typ.Optional[int] = 0,
) -> typ.List[Article]: ...


def get_article_by_slug(db_conn: Connection, slug: str) -> Article: ...


def create_article(
    db_conn: Connection, curr_user_id: str, data: CreateArticleData
) -> Article: ...


def update_article(
    db_conn: Connection, slug: str, curr_user_id: str, data: UpdateArticleData
) -> Article: ...


def delete_article(db_conn: Connection, slug: str, curr_user_id: str) -> bool: ...


def create_article_comment(
    db_conn: Connection, slug: str, curr_user_id: str, data: CreateCommentData
) -> typ.Tuple[bool, Comment]: ...


def get_article_comments(
    db_conn: Connection, slug: str
) -> typ.Tuple[bool, typ.List[Comment]]: ...


def delete_article_comment(
    db_conn: Connection, slug: str, comment_id: int, curr_user_id: str
) -> typ.Tuple[bool, bool]: ...


def add_article_favorite(
    db_conn: Connection, article_id: int, curr_user_id: str
) -> Article: ...


def delete_article_favorite(
    db_conn: Connection, article_id: int, curr_user_id: str
) -> Article: ...


def get_all_tags(db_conn: Connection) -> typ.List[str]: ...
