from flask import Blueprint, request
from realworld.db import get_db_connection
from realworld.api.handlers.articles import (
    fetch_articles
)
from realworld.api.models.articles import (
    GetArticlesQueryParams,
    GetFeedQueryParams,
    CreateArticleRequest,
    UpdateArticleRequest,
    CreateCommentRequest,
    SingleArticleResponse,
    MultipleArticlesResponse,
    DeleteArticleResponse,
    SingleCommentResponse,
    ArticleCommentsResponse,
    DeleteCommentResponse,
)

articles_blueprint = Blueprint("articles_endpoints", __name__, url_prefix="/articles")


@articles_blueprint.route("", methods=["GET"])
# def get_articles() -> MultipleArticlesResponse:
def get_articles():
    """
    Returns most recent articles globally.
    """

    params = {}
    if request.args:
        params_model = GetArticlesQueryParams(**request.args)
        params = params_model.model_dump()
        print(f"parsed: {params}")

    # TODO: (@mhegel) handle pagination
    with get_db_connection() as db_conn:
        data = fetch_articles(db_conn, **params)

    # order data, return data
    return data


@articles_blueprint.route("/feed", methods=["GET"])
def get_feed() -> MultipleArticlesResponse:
    """
    Authentication required.  Returns most recent articles created by followed users.
    """

    if request.args:
        qparams = GetFeedQueryParams(**request.args)
        print(f"parsed: {qparams.model_dump()}")

    # validate query params
    return {
        "articles": [
            {
                "slug": "how-to-article",
                "title": "How to Article",
                "description": "A test article.",
                "body": "This is just a test!",
                "tagList": ["test", "article"],
                "createdAt": "2023-12-14T06:31:55.398685+00:00",
                "updatedAt": "2023-12-14T06:31:55.398685+00:00",
                "favorited": True,
                "favoritesCount": 1,
                "author": {
                    "username": "user",
                    "bio": "I am a user.",
                    "image": None,
                    "following": False,
                },
            }
        ]
    }


@articles_blueprint.route("/<string:slug>", methods=["GET"])
def get_article(slug: str) -> SingleArticleResponse:
    return {
        "article": {
            "slug": slug,
            "title": "How to Article",
            "description": "A test article.",
            "body": "This is just a test!",
            "tagList": ["test", "article"],
            "createdAt": "2023-12-14T06:31:55.398685+00:00",
            "updatedAt": "2023-12-14T06:31:55.398685+00:00",
            "favorited": True,
            "favoritesCount": 1,
            "author": {
                "username": "user",
                "bio": "I am a user.",
                "image": None,
                "following": False,
            },
        }
    }


@articles_blueprint.route("", methods=["POST"])
def create_article() -> SingleArticleResponse:
    """
    Authentication required.
    """

    request_model = CreateArticleRequest()
    request_model.model_validate_json(request.json)
    return {
        "article": {
            "slug": "how-to-article",
            "title": "How to Article",
            "description": "A test article.",
            "body": "This is just a test!",
            "tagList": ["test", "article"],
            "createdAt": "2023-12-14T06:31:55.398685+00:00",
            "updatedAt": "2023-12-14T06:31:55.398685+00:00",
            "favorited": True,
            "favoritesCount": 1,
            "author": {
                "username": "user",
                "bio": "I am a user.",
                "image": None,
                "following": False,
            },
        }
    }


@articles_blueprint.route("/<string:slug>", methods=["PUT"])
def update_article(slug) -> SingleArticleResponse:
    """
    Authentication required.
    """
    request_model = UpdateArticleRequest()
    request_model.model_validate_json(request.json)
    return {
        "article": {
            "slug": slug,
            "title": "How to Article 2.0",
            "description": "A test article.",
            "body": "This is just a test!",
            "tagList": ["test", "article"],
            "createdAt": "2023-12-14T06:31:55.398685+00:00",
            "updatedAt": "2023-12-14T06:31:55.398685+00:00",
            "favorited": True,
            "favoritesCount": 1,
            "author": {
                "username": "user",
                "bio": "I am a user.",
                "image": None,
                "following": False,
            },
        }
    }


@articles_blueprint.route("/<string:slug>", methods=["DELETE"])
def delete_article(slug: str) -> DeleteArticleResponse:
    return {"message": f"Article `{slug}` successfully deleted."}


#
# Comments
#


@articles_blueprint.route("/<string:slug>/comments", methods=["POST"])
def create_comment(slug: str) -> SingleCommentResponse:
    request_model = CreateCommentRequest()
    request_model.model_validate_json(request.json)
    return {
        "comment": {
            "id": 1,
            "createdAt": "2023-12-14T06:31:55.398685+00:00",
            "updatedAt": "2023-12-14T06:31:55.398685+00:00",
            "body": "What a nice article!",
            "author": {
                "username": "user",
                "bio": "I am a user.",
                "image": None,
                "following": False,
            },
        }
    }


@articles_blueprint.route("/<string:slug>/comments", methods=["GET"])
def get_comments(slug: str) -> ArticleCommentsResponse:
    return {
        "comments": [
            {
                "id": 1,
                "createdAt": "2023-12-14T06:31:55.398685+00:00",
                "updatedAt": "2023-12-14T06:31:55.398685+00:00",
                "body": "What a nice article!",
                "author": {
                    "username": "user",
                    "bio": "I am a user.",
                    "image": None,
                    "following": False,
                },
            }
        ]
    }


@articles_blueprint.route("/<string:slug>/comments/<string:id>", methods=["DELETE"])
def delete_comment(slug: str, id: str) -> DeleteCommentResponse:
    return {"message": f"Comment {id} from Article {slug} successfully deleted."}


#
# Favorites
#


@articles_blueprint.route("/<string:slug>/favorite", methods=["POST"])
def favorite_article(slug: str) -> SingleArticleResponse:
    return {
        "article": {
            "slug": slug,
            "title": "How to Article 2.0",
            "description": "A test article.",
            "body": "This is just a test!",
            "tagList": ["test", "article"],
            "createdAt": "2023-12-14T06:31:55.398685+00:00",
            "updatedAt": "2023-12-14T06:31:55.398685+00:00",
            "favorited": True,
            "favoritesCount": 1,
            "author": {
                "username": "user",
                "bio": "I am a user.",
                "image": None,
                "following": False,
            },
        }
    }


@articles_blueprint.route("/<string:slug>/favorite", methods=["DELETE"])
def unfavorite_article(slug: str) -> SingleArticleResponse:
    return {
        "article": {
            "slug": slug,
            "title": "How to Article 2.0",
            "description": "A test article.",
            "body": "This is just a test!",
            "tagList": ["test", "article"],
            "createdAt": "2023-12-14T06:31:55.398685+00:00",
            "updatedAt": "2023-12-14T06:31:55.398685+00:00",
            "favorited": True,
            "favoritesCount": 1,
            "author": {
                "username": "user",
                "bio": "I am a user.",
                "image": None,
                "following": False,
            },
        }
    }
