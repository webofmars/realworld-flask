import re
import typing as typ
from uuid import uuid4
from sqlalchemy.engine import Connection
from sqlalchemy.sql import text as satext
from realworld.api.core.models import Article, Profile, Comment

# from realworld.api.handlers.queries import get_articles_query
from realworld.api.routes.v1.articles.models import (
    CreateArticleData,
    UpdateArticleData,
    CreateCommentData,
)

#
# Helpers
#


# return a URL-friendly article slug that likely unique
def generate_slug(title: str) -> str:
    title.lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-_]", "", slug)
    return f"{slug}-{uuid4().hex[:8]}"


def _get_curr_profile_by_id(db_conn: Connection, user_id: str) -> Profile:
    result = db_conn.execute(
        satext(
            """
            SELECT username, bio, image
            FROM users
            WHERE id = :user_id
            """
        ).bindparams(user_id=user_id)
    ).fetchone()

    return Profile(
        username=result.username,
        bio=result.bio,
        image=result.image.decode() if result.image else None,
        following=None,  # NOTE: can't follow yourself
    )


def _get_article_by_id(
    db_conn: Connection, article_id: int, curr_user_id: typ.Optional[str]
) -> typ.Optional[Article]:
    result = db_conn.execute(
        satext(
            """
            SELECT
                a.id,
                a.slug,
                a.title,
                a.description,
                a.body,
                a.tag_list,
                a.created_date,
                a.updated_date,
                u.username AS author_username,
                u.bio AS author_bio,
                u.image AS author_image,
                (
                    SELECT COUNT(*)
                    FROM favorites f
                    WHERE f.article_id = a.id
                ) AS favorites_count,
                (
                    SELECT COUNT(*)
                    FROM favorites f
                    WHERE f.article_id = a.id AND f.user_id = :curr_user_id
                ) AS favorited_by_curr_user
                (
                    SELECT COUNT(*)
                    FROM user_follows uf
                    WHERE uf.user_id = :curr_user_id
                    AND uf.following_user_id = u.id
                ) > 0 AS is_curr_user_following
            FROM articles a
            JOIN users u ON a.author_id = u.id
            WHERE a.id = :article_id
            """
        ).bindparams(article_id=article_id, curr_user_id=curr_user_id)
    ).fetchone()

    if not result:
        return None

    return Article(
        id=result.id,
        slug=result.slug,
        title=result.title,
        description=result.description,
        body=result.body,
        tag_list=result.tag_list,
        created_date=result.created_date,
        updated_date=result.updated_date,
        favorites_count=result.favorites_count,
        favorited_by_curr_user=bool(result.favorited_by_curr_user),
        author=Profile(
            bio=result.author_bio,
            username=result.author_username,
            following=result.is_curr_user_following,
            image=result.author_image.decode() if result.author_image else None,
        ),
    )


#
# Handlers
#


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


def get_article_by_slug(
    db_conn: Connection, slug: str, curr_user_id: typ.Optional[str]
) -> typ.Optional[Article]:
    result = db_conn.execute(
        satext(
            """
            SELECT
                a.id,
                a.slug,
                a.title,
                a.description,
                a.body,
                a.tag_list,
                a.created_date,
                a.updated_date,
                u.username AS author_username,
                u.bio AS author_bio,
                u.image AS author_image,
                (
                    SELECT COUNT(*)
                    FROM favorites f
                    WHERE f.article_id = a.id
                ) AS favorites_count,
                (
                    SELECT COUNT(*)
                    FROM favorites f
                    WHERE f.article_id = a.id AND f.user_id = :curr_user_id
                ) AS favorited_by_curr_user
                (
                    SELECT COUNT(*)
                    FROM user_follows uf
                    WHERE uf.user_id = :curr_user_id
                    AND uf.following_user_id = u.id
                ) > 0 AS is_curr_user_following
            FROM articles a
            JOIN users u ON a.author_id = u.id
            WHERE a.slug = :slug
            """
        ).bindparams(slug=slug, curr_user_id=curr_user_id)
    ).fetchone()

    if not result:
        return None

    return Article(
        id=result.id,
        slug=result.slug,
        title=result.title,
        description=result.description,
        body=result.body,
        tag_list=result.tag_list,
        created_date=result.created_date,
        updated_date=result.updated_date,
        favorites_count=result.favorites_count,
        favorited_by_curr_user=bool(result.favorited_by_curr_user),
        author=Profile(
            bio=result.author_bio,
            username=result.author_username,
            following=result.is_curr_user_following,
            image=result.author_image.decode() if result.author_image else None,
        ),
    )


def create_article(
    db_conn: Connection, curr_user_id: str, data: CreateArticleData
) -> Article:
    slug = generate_slug(data.title)
    db_conn.execute(
        satext(
            """
            INSERT INTO articles (author_id, slug, title, description, body, tag_list)
            VALUES (:author_id, :slug, :title, :description, :body, :tag_list)
            """
        ).bindparams(
            author_id=curr_user_id,
            slug=slug,
            title=data.title,
            description=data.description,
            body=data.body,
            tag_list=data.tag_list,
        )
    )
    return get_article_by_slug(db_conn, slug, curr_user_id)


def update_article(
    db_conn: Connection, slug: str, curr_user_id: str, data: UpdateArticleData
) -> Article:

    update_str = ""
    params = {}
    for key in ("title", "description", "body"):
        if value := getattr(data, key):
            update_str += f"{key} = :{key}, "
            params[key] = value

    slug = generate_slug(data.title)
    db_conn.execute(
        satext(
            f"""
            UPDATE articles
            SET {update_str}
                updated_date = CURRENT_TIMESTAMP
            WHERE slug = :slug
            AND author_id = :curr_user_id
            """
        ).bindparams(
            slug=slug,
            curr_user_id=curr_user_id,
            **params,
        )
    )
    return get_article_by_slug(db_conn, slug, curr_user_id)


def delete_article(db_conn: Connection, slug: str, curr_user_id: str) -> bool:
    result = db_conn.execute(
        satext(
            """
            DELETE FROM articles
            WHERE slug = :slug
            AND author_id = :curr_user_id
            """
        ).bindparams(slug=slug, curr_user_id=curr_user_id)
    )
    return bool(result.rowcount)


def create_article_comment(
    db_conn: Connection, slug: str, curr_user_id: str, data: CreateCommentData
) -> typ.Tuple[bool, Comment]:
    result = db_conn.execute(
        satext(
            """
            INSERT INTO article_comments (article_id, commenter_user_id, body)
            VALUES (
                (SELECT id FROM articles WHERE slug = :slug),
                :curr_user_id,
                :body
            )
            RETURNING id, created_date
            """
        ).bindparams(slug=slug, curr_user_id=curr_user_id, body=data.body)
    ).fetchone()

    if not result:
        return False, None

    return True, Comment(
        id=result.id,
        created_at=result.created_date,
        updated_at=result.created_date,
        body=data.body,
        author=_get_curr_profile_by_id(db_conn, curr_user_id),
    )


def get_article_comments(
    db_conn: Connection, slug: str, curr_user_id: typ.Optional[str]
) -> typ.Tuple[bool, typ.List[Comment]]:
    result = db_conn.execute(
        satext(
            """
            SELECT
                ac.id,
                ac.body,
                ac.created_date,
                ac.updated_date,
                u.username,
                u.bio,
                u.image,
                (
                    SELECT COUNT(*)
                    FROM user_follows uf
                    WHERE uf.user_id = :curr_user_id
                    AND uf.following_user_id = u.id
                ) > 0 AS is_following
            FROM article_comments ac
            JOIN users u ON ac.commenter_user_id = u.id
            JOIN articles a ON ac.article_id = a.id
            WHERE a.slug = :slug
            """
        ).bindparams(slug=slug, curr_user_id=curr_user_id)
    ).fetchall()

    if not result:
        return False, []

    comments = []
    for row in result:
        comments.append(
            Comment(
                id=row.id,
                body=row.body,
                created_at=row.created_date,
                updated_at=row.updated_date,
                author=Profile(
                    username=row.username,
                    bio=row.bio,
                    image=row.image.decode() if row.image else None,
                    following=row.is_following,
                ),
            )
        )

    return True, comments


def delete_article_comment(
    db_conn: Connection, slug: str, comment_id: int, curr_user_id: str
) -> bool:
    """Returns (does_article_exist)"""
    result = db_conn.execute(
        satext(
            """
            DELETE FROM article_comments
            WHERE id = :comment_id
            AND article_id = (SELECT id FROM articles WHERE slug = :slug)
            AND commenter_user_id = :curr_user_id
            """
        ).bindparams(slug=slug, comment_id=comment_id, curr_user_id=curr_user_id)
    )
    return True


def add_article_favorite(
    db_conn: Connection, article_id: int, curr_user_id: str
) -> typ.Optional[Article]:
    db_conn.execute(
        satext(
            """
            INSERT INTO article_favorites (article_id, user_id)
            VALUES (:article_id, :user_id)
            ON CONFLICT DO NOTHING
            """
        ).bindparams(article_id=article_id, user_id=curr_user_id)
    )
    return _get_article_by_id(db_conn, article_id, curr_user_id)


def delete_article_favorite(
    db_conn: Connection, article_id: int, curr_user_id: str
) -> typ.Optional[Article]:
    db_conn.execute(
        satext(
            """
            DELETE FROM article_favorites
            WHERE article_id = :article_id
            AND user_id = :user_id
            """
        ).bindparams(article_id=article_id, user_id=curr_user_id)
    )
    return _get_article_by_id(db_conn, article_id, curr_user_id)


# TODO: store tags in a separate table with association table
def get_all_tags(db_conn: Connection) -> typ.List[str]:
    result = db_conn.execute(
        satext(
            """
            SELECT DISTINCT UNNEST(tag_list) AS tag
            FROM articles
            """
        )
    ).fetchall()
    return [row.tag for row in result]
