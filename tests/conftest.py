"""Flask tests config."""
import pytest

from GUI import app as flask_app


@pytest.fixture
def app():
    """Initialize Flask."""
    yield flask_app


@pytest.fixture
def client(app):
    """Initialize Flask."""
    return app.test_client()
