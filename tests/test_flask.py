"""Checks that flask opened correctly."""


def test_index(app, client):
    """Checks that flask resolves a 200 code"""
    res = client.get("/")
    assert res.status_code == 200
