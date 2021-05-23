import pytest

from GUI import app as flask_app

@pytest.fixture
def app():
	yield flask_app

@pytest.fixture
def client(app):
	return app.test_client()
