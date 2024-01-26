from flask import Flask
from realworld.api.routes.v1.articles import articles_blueprint
from realworld.api.routes.v1.users import users_blueprint
from realworld.api.routes.v1.profiles import profiles_blueprint
from realworld.api.routes.v1.tags import tags_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    _register_blueprints(app)
    return app


def _register_blueprints(app: Flask):
    app.register_blueprint(
        articles_blueprint, url_prefix=f"/api{articles_blueprint.url_prefix}"
    )
    app.register_blueprint(
        # no `url_prefix` because of separate `/user` and `/users` endpoints
        users_blueprint,
        url_prefix="/api",
    )
    app.register_blueprint(
        profiles_blueprint, url_prefix=f"/api{profiles_blueprint.url_prefix}"
    )
    app.register_blueprint(
        tags_blueprint, url_prefix=f"/api{tags_blueprint.url_prefix}"
    )


app = create_app()
