from flask import Blueprint


users_blueprint = Blueprint(
    "users_endpoints", __name__,
)


@users_blueprint.route("/users", methods=["POST"])
def create_user():
    """
    POST Body
        {
            "user":{
                "username": "User",
                "email": "user@realworld.io",
                "password": "password"
            }
        }
    """
    # data = request.get_json()
    return {
        "profile": {
            "username": "user",
            "bio": "I am a user.",
            "image": None,
            "following": False
        }
   }

@users_blueprint.route("/users/login", methods=["POST"])
def authenticate_user():
    """
    POST Body
        {
            "user": {
                "email": "user@realworld.io",
                "password": "password"
            }
        }
    """
    # data = request.get_json()
    return {
        "user": {
            "email": "user@realworld.io",
            "token": "jwt.token.here",
            "username": "user",
            "bio": "I am a user.",
            "image": None
        }
    }


@users_blueprint.route("/user", methods=["GET"])
def get_current_user():
    return {
        "profile": {
            "username": "user",
            "bio": "I am a user.",
            "image": None,
            "following": False
        }
    }


@users_blueprint.route("/user", methods=["PUT"])
def update_user():
    """
    PUT Body
        {
            "user":{
                "email": "user@realworld.io",
                "bio": "I am an updated user.",
                "image": None
            }
        }
    """
    return {
        "user": {
            "email": "user@realworld.io",
            "token": "jwt.token.here",
            "username": "user",
            "bio": "I am a user.",
            "image": None
        }
    }
