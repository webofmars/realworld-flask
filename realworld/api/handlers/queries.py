import typing as typ
from sqlalchemy import TextClause, text as satext


def get_articles_query(
    user_id: str,
    *,
    tags: typ.Optional[typ.List[str]] = None,
    author_username: typ.Optional[str] = None,
    is_favorited: typ.Optional[bool] = None,
    is_feed: typ.Optional[bool] = False
) -> TextClause:

    # TODO: (@mhegel) ensure only valid param combinations are allowed

    base_query = """
    SELECT
        a.id AS article_id,
        a.title,
        a.slug,
        a.description,
        a.body,
        a.created_date,
        a.updated_date,
        a.tags,
        u.username AS author_username,
        u.id AS author_id,
        u.bio AS author_bio,
        u.image AS author_image
    FROM
        articles a
    JOIN
        users u ON a.author_user_id = u.id
    WHERE
    """

    params = {}
    conditions = []

    if tags:
        params["tags"] = tags
        conditions.append("(ARRAY[:tags]::text[] <@ a.tags OR :tags IS NULL)")

    if author_username:
        params["author"] = author_username
        conditions.append("(u.username = :author OR :author IS NULL)")

    if is_favorited:
        params["favorites_user_id"] = user_id
        conditions.append(
            "(a.id IN (SELECT article_id FROM article_favorites WHERE user_id = :favorites_user_id) OR :favorites_user_id IS NULL)"
        )

    if is_feed:
        params["feed_user_id"] = user_id
        conditions.append(
            "(a.author_user_id IN (SELECT follows_user_id FROM user_follows WHERE user_id = :user_id) OR :user_id IS NULL)"
        )

    if conditions:
        query = base_query + " AND ".join(conditions)
    else:
        query = base_query.replace("WHERE", "")

    return satext(query).bindparams(**params)
