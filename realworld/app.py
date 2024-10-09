from flask import Flask
from flask_cors import CORS
from realworld.api.routes.v1.users.routes import users_blueprint
from realworld.api.routes.v1.profiles.routes import profiles_blueprint
from realworld.api.routes.v1.articles.routes import articles_blueprint, tags_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    _register_blueprints(app)
    return app


def _register_blueprints(app: Flask):
    app.register_blueprint(articles_blueprint, url_prefix="/api")
    app.register_blueprint(users_blueprint, url_prefix="/api")
    app.register_blueprint(
        profiles_blueprint, url_prefix=f"/api{profiles_blueprint.url_prefix}"
    )
    app.register_blueprint(
        tags_blueprint, url_prefix=f"/api{tags_blueprint.url_prefix}"
    )
    @app.route("/api/ping")
    def ping():
        return "pong"


app = create_app()
