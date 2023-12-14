from flask import Blueprint

profiles_blueprint = Blueprint(
    "profiles_endpoints", __name__, url_prefix="/profiles"
)


@profiles_blueprint.route("/<string:username>", methods=["GET"])
def get_profile(username):
    """
    Authentication optional.
    """
    print(username)
    return {
        "profile": {
            "username": username,
            "bio": "I am a user.",
            "image": None,
            "following": False
        }
   }


@profiles_blueprint.route("/<string:username>/follow", methods=["POST"])
def follow_profile(username):
    """
    Authentication required.
    """
    print(username)
    return {
        "profile": {
            "username": username,
            "bio": "I am a user.",
            "image": None,
            "following": False
        }
   }


@profiles_blueprint.route("/<string:username>/follow", methods=["DELETE"])
def unfollow_profile(username):
    """
    Authentication required.
    """
    print(username)
    return {
        "profile": {
            "username": username,
            "bio": "I am a user.",
            "image": None,
            "following": False
        }
   }
