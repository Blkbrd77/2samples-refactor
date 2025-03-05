import pytest
import subprocess
from app.main import app
from app.config import CLOUDFRONT_DOMAIN, IMAGE_PATH


@pytest.fixture
def client():
    return app.test_client()


def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"TRAVELS" in response.data
    assert b'href="/japan2019"' in response.data
    assert b'href="/ireland"' in response.data
    assert b'href="/uk"' in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data
    assert b'class="tile"' in response.data
    assert f"{CLOUDFRONT_DOMAIN}{IMAGE_PATH}IMG_3137.jpeg".encode() in response.data
    assert f"{CLOUDFRONT_DOMAIN}{IMAGE_PATH}RenderedImage.jpeg".encode() in response.data
    assert f"{CLOUDFRONT_DOMAIN}{IMAGE_PATH}IMG_3305-225x300.jpeg".encode() in response.data


def test_japan2019_page():
    client = app.test_client()
    response = client.get('/japan2019')
    assert response.status_code == 200
    assert b"JAPAN 2019" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


def test_ireland_page():
    client = app.test_client()
    response = client.get('/ireland')
    assert response.status_code == 200
    assert b"REPUBLIC OF IRELAND" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


def test_uk_page():
    client = app.test_client()
    response = client.get('/uk')
    assert response.status_code == 200
    assert b"UNITED KINGDOM" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


def test_blog_page():
    client = app.test_client()
    response = client.get('/blog')
    assert response.status_code == 200
    assert b"Blog" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


def test_maps_page():
    client = app.test_client()
    response = client.get('/maps')
    assert response.status_code == 200
    assert b"Maps" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


def test_privacy_page():
    client = app.test_client()
    response = client.get('/privacy')
    assert response.status_code == 200
    assert b"Privacy Policy" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


def test_flask_installed():
    result = subprocess.run(["pip", "show", "flask"], capture_output=True, text=True)
    assert "Name: Flask" in result.stdout


def test_pytest_installed():
    result = subprocess.run(["pip", "show", "pytest"], capture_output=True, text=True)
    assert "Name: pytest" in result.stdout
