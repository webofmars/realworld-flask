from flask import Blueprint

articles_blueprint = Blueprint(
    "articles_endpoints", __name__, url_prefix="/articles"
)


@articles_blueprint.route("", methods=["GET"])
def get_articles():
    """
    Authentication optional.

    Default:
        Returns most recent articles globally.

    Query params:
        - tag
        - author
        - favorited by user
        - limit = 20
        - offset = 0
    """
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
                    "following": False
                }
            }
        ]
    }


@articles_blueprint.route("/feed", methods=["GET"])
def get_feed():
    """
    Authentication required.

    Default:
        Returns most recent articles created by followed users.

    Query params:
        - limit = 20
        - offset = 0
    """
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
                    "following": False
                }
            }
        ]
    }


@articles_blueprint.route("/<string:slug>", methods=["GET"])
def get_article(slug):
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
                "following": False
            }
        }
    }


@articles_blueprint.route("", methods=["POST"])
def create_article():
    """
    Authentication required.

    POST Body
        {
            "article": {
                "title": "How to Article",
                "description": "A test article.",
                "body": "This is just a test!",
                "tagList": ["test", "article"]
            }
        }
    """

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
                "following": False
            }
        }
    }


@articles_blueprint.route("/<string:slug>", methods=["PUT"])
def update_article(slug):
    """
    Authentication required.

    PUT Body
        {
            "article": {
                "title": "How to Article 2.0"
            }
        }
    """
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
                "following": False
            }
        }
    }


@articles_blueprint.route("/<string:slug>", methods=["DELETE"])
def delete_article(slug):
    return {
        "message": f"Article `{slug}` successfully deleted."
    }

#
# Comments
#

@articles_blueprint.route("/<string:slug>/comments", methods=["POST"])
def add_comment(slug):
    """
    POST Body
        {
            "comment": {
                "body": "What a nice article!"
            }
        }
    """
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
                "following": False
            }
        }
    }


@articles_blueprint.route("/<string:slug>/comments", methods=["GET"])
def get_comments(slug):
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
                    "following": False
                }
            }
        ]
    }


@articles_blueprint.route("/<string:slug>/comments/<string:id>", methods=["DELETE"])
def delete_comment(slug, id):
    return {
        "message": f"Comment {id} from Article {slug} successfully deleted."
    }

#
# Favorites
#


@articles_blueprint.route("/<string:slug>/favorite", methods=["POST"])
def favorite_article(slug):
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
                "following": False
            }
        }
    }


@articles_blueprint.route("/<string:slug>/favorite", methods=["DELETE"])
def unfavorite_article(slug):
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
                "following": False
            }
        }
    }