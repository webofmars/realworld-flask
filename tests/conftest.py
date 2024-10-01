from random import randint
from uuid import uuid4
from pytest import fixture
from unittest.mock import patch
from realworld.app import create_app
from sqlalchemy import text as satext
from datetime import datetime, timezone as tz
from realworld.api.core.db import _ENGINE, _Session
from realworld.api.routes.v1.users.handler import hash_password

# from realworld.api.core.auth import generate_jwt
# from .data import SESSION_USER_ID, SESSION_USER_NAME


####################
# App Fixtures
####################


@fixture(scope="session")
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@fixture(scope="session")
def client(test_app):
    return test_app.test_client()


###########################################################
# DB Fixtures (rollback transaction after each unit test) #
###########################################################


@fixture(scope="session")
def mock_conn():
    connection = _ENGINE.connect()
    yield connection
    connection.close()


@fixture(scope="function")
def mock_db_session(mock_conn):
    transaction = mock_conn.begin()
    session = _Session(bind=mock_conn)
    yield session
    session.close()
    transaction.rollback()


@fixture(autouse=True)
def mock_get_db_connection(mock_db_session):
    with patch("realworld.api.core.db._create_db_connection") as mock_db_conn:
        mock_db_conn.return_value = mock_db_session, mock_db_session.connection()
        yield mock_db_conn


####################
# Data Fixtures
####################


@fixture(scope="function")
def add_user(mock_db_session):
    def _add_user(
        _id=None,
        username=None,
        email=None,
        password=None,
        image=None,
        bio=None,
        ts=None,
    ):
        _id = _id or str(uuid4())
        ts = ts or datetime.now(tz.utc).isoformat()
        username = username or f"mock-user-{_id}"
        password = password or "password"
        image = image or None
        user = {
            "id": _id,
            "username": username,
            "email": email or f"{username}@realworld.io",
            "bio": bio or f"mock bio for {username}",
            "image": image.encode() if image else None,
            "password_hash": hash_password(password or "password"),
            "created_date": ts,
            "updated_date": ts,
        }
        stmt = satext(
            """
            INSERT INTO users (id, username, email, password_hash, image, bio, created_date, updated_date)
            VALUES (:id, :username, :email, :password_hash, :image, :bio, :created_date, :updated_date)
            """
        ).bindparams(**user)
        mock_db_session.execute(stmt)

        # Reset user dict before returning
        user.pop("password_hash")
        user["password"] = password
        user["image"]

        return user

    return _add_user


# @fixture(scope="session")
# def session_user(add_user):
#     return add_user(_id=SESSION_USER_ID, username=SESSION_USER_NAME)


# @fixture(scope="function")
# def session_user_token(session_user):
#     return generate_jwt(session_user["id"])


@fixture(scope="function")
def add_user_follow(mock_db_session):
    def _add_user_follow(user_id=None, follows_user_id=None):
        user_follow = {
            "user_id": user_id or str(uuid4()),
            "follows_user_id": follows_user_id or str(uuid4()),
        }

        stmt = satext(
            """
            INSERT INTO user_follows (user_id, follows_user_id)
            VALUES (:user_id, :follows_user_id)
            """
        )
        mock_db_session.execute(stmt, user_follow)

        return user_follow

    return _add_user_follow


@fixture(scope="function")
def add_article(mock_db_session, add_user):
    def _add_article(
        _id=None,
        author_user_id=None,
        slug=None,
        title=None,
        description=None,
        body=None,
        tags=None,
        ts=None,
    ):
        _id = _id or str(uuid4())
        ts = ts or datetime.now(tz.utc).isoformat()
        article = {
            "id": _id,
            "author_user_id": author_user_id or add_user(),
            "slug": slug or f"mock-slug-{_id}",
            "title": title or f"Mock Title ({_id})",
            "description": description or f"Mock description of `Mock Title ({_id})`",
            "body": body or f"Mock body of `Mock Title ({_id})`",
            "tags": tags or ["mock"],
            "created_date": ts,
            "updated_date": ts,
        }

        stmt = satext(
            """
            INSERT INTO articles (id, author_user_id, slug, title, description, body, tags, created_date, updated_date)
            VALUES (:id, :author_user_id, :slug, :title, :description, :body, :tags, :created_date, :updated_date)
            """
        )
        mock_db_session.execute(stmt, article)

        return article

    return _add_article


@fixture(scope="function")
def add_article_favorite(mock_db_session):
    def _add_article_favorite(user_id=None, article_id=None):
        article_favorite = {
            "user_id": user_id or str(uuid4()),
            "article_id": article_id or str(uuid4()),
        }

        stmt = satext(
            """
            INSERT INTO article_favorites (user_id, article_id)
            VALUES (:user_id, :article_id)
            """
        )
        mock_db_session.execute(stmt, article_favorite)

        return article_favorite

    return _add_article_favorite


@fixture(scope="function")
def add_article_comment(mock_db_session):
    def _add_article_comment(
        _id=None, article_id=None, commenter_user_id=None, body=None, ts=None
    ):
        _id = _id or str(uuid4())
        ts = ts or datetime.now(tz.utc).isoformat()
        article_comment = {
            "id": _id,
            "article_id": article_id or str(uuid4()),
            "commenter_user_id": commenter_user_id or str(uuid4()),
            "body": body or f"Mock comment body for article {article_id}",
            "created_date": ts,
            "updated_date": ts,
        }

        stmt = satext(
            """
            INSERT INTO article_comments (id, article_id, commenter_user_id, body, created_date, updated_date)
            VALUES (:id, :article_id, :commenter_user_id, :body, :created_date, :updated_date)
            """
        )
        mock_db_session.execute(stmt, article_comment)

        return article_comment

    return _add_article_comment


@fixture(scope="function")
def add_tag(mock_db_session):
    def _add_tag(tag=None):
        tag = tag or f"mock-tag-{randint(0, 100)}"
        stmt = satext(
            """
            INSERT INTO tags (tag)
            VALUES (:tag)
            """
        )
        mock_db_session.execute(stmt, {"tag": tag})
        return tag

    return _add_tag


@fixture(scope="function")
def add_article_tag(mock_db_session):
    def _add_article_tag(article_id=None, tag=None):
        article_tag = {
            "article_id": article_id or str(uuid4()),
            "tag": tag or f"mock-tag-{randint(0, 100)}",
        }

        stmt = satext(
            """
            INSERT INTO article_tags (article_id, tag)
            VALUES (:article_id, :tag)
            """
        )
        mock_db_session.execute(stmt, article_tag)

        return article_tag

    return _add_article_tag
