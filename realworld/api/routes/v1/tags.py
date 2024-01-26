from flask import Blueprint
from realworld.api.models.tags import TagsResponse

tags_blueprint = Blueprint("tags_endpoints", __name__, url_prefix="/tags")


@tags_blueprint.route("", methods=["GET"])
def get_tags() -> TagsResponse:
    return {"tags": ["test", "article"]}
