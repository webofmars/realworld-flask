from flask import Blueprint

tags_blueprint = Blueprint(
    "tags_endpoints", __name__, url_prefix="/tags"
)


@tags_blueprint.route("", methods=["GET"])
def get_tags():
    return {
        "tags": [
            "test",
            "article"
        ]
    }
