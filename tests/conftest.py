import pytest
from fincrypt import create_app, db
import os
test_db_path = "fincrypt/test_fincrypt.db"


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    # other setup can go here
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test_fincrypt.db"

    })
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def cleaning_test_db():
    if os.path.isfile(test_db_path):
        os.remove(test_db_path)
