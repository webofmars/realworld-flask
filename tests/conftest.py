from pytest import fixture
from realworld.app import create_app


@fixture(scope="session")
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@fixture(scope="session")
def client(test_app):
    return test_app.test_client()
