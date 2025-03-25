import pytest
from app.main import app
import subprocess
import requests


# Use Flask's test client as a fixture
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route_renders_images(client):
    """Test that the index route renders HTML with CloudFront image URLs."""
    response = client.get('/')
    assert response.status_code == 200  # Check the route loads successfully

    # Convert response data to string (it's bytes by default)
    html = response.data.decode('utf-8')  # Check for each image URL in the rendered HTML
    assert 'https://d1rhrn7ca7di1b.cloudfront.net/images/IMG_3137.jpeg' in html
    assert 'https://d1rhrn7ca7di1b.cloudfront.net/images/RenderedImage.jpeg' in html
    assert 'https://d1rhrn7ca7di1b.cloudfront.net/images/IMG_3305-225x300.jpeg' in html


def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'href="/japan"' in response.data
    assert b'href="/ireland"' in response.data
    assert b'href="/uk"' in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data
    assert b'class="tile"' in response.data


def test_japan_page():
    client = app.test_client()
    response = client.get('/japan')
    assert response.status_code == 200
    assert b"JAPAN" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


def test_ireland_page():
    client = app.test_client()
    response = client.get('/ireland')
    assert response.status_code == 200
    assert b"REPUBLIC OF IRELAND" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


@pytest.fixture
def mock_s3_ireland(monkeypatch):
    class MockS3Client:
        def list_objects_v2(self, Bucket, Prefix):
            if Prefix == 'videos/':
                return {
                    'Contents': [
                        {'Key': 'videos/Ireland-Scotland-Day-One.mov'},
                        {'Key': 'videos/Ireland-Scotland-Day-Two.mov'},
                        {'Key': 'videos/Ireland-Scotland-Day-Three.mov'},
                        {'Key': 'videos/Ireland-Scotland-Day-Four.mov'}
                    ]
                }
            elif Prefix == 'stills/':
                return {
                    'Contents': [
                        {'Key': 'stills/Ireland-Scotland-Day-One-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-Day-Two-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-Day-Three-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-Day-Four-still-001.jpg'}
                    ]
                }
            return {'Contents': []}
    monkeypatch.setattr('app.main.s3_client', MockS3Client())


@pytest.fixture
def mock_s3_japan(monkeypatch):
    class MockS3Client:
        def list_objects_v2(self, Bucket, Prefix):
            if Prefix == 'videos/':
                return {
                    'Contents': [
                        {'Key': 'videos/Japan-2019-Osaka.mov'},
                        {'Key': 'videos/Japan-2019.mov'},
                    ]
                }
            elif Prefix == 'stills/':
                return {
                    'Contents': [
                        {'Key': 'stills/Japan-2019-Osaka-still-001.jpg'},
                        {'Key': 'stills/Japan-2019-still-001.jpg'},
                    ]
                }
            return {'Contents': []}
    monkeypatch.setattr('app.main.s3_client', MockS3Client())

@pytest.fixture
def mock_s3_uk(monkeypatch):
    class MockS3Client:
        def list_objects_v2(self, Bucket, Prefix):
            if Prefix == 'videos/':
                return {
                    'Contents': [
                        {'Key': 'videos/Ireland-Scotland-Day-Five.mov'},
                        {'Key': 'videos/Ireland-Scotland-Day-Six.mov'},
                        {'Key': 'videos/Ireland-Scotland-Day-Seven.mov'},
                        {'Key': 'videos/Ireland-Scotland-Day-Eight.mov'},
                        {'Key': 'videos/Ireland-Scotland-England-Day-Nine.mov'}
                    ]
                }
            elif Prefix == 'stills/':
                return {
                    'Contents': [
                        {'Key': 'stills/Ireland-Scotland-Day-Five-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-Day-Six-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-Day-Seven-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-Day-Eight-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-England-Day-Nine-still-001.jpg'}
                    ]
                }
            return {'Contents': []}
    monkeypatch.setattr('app.main.s3_client', MockS3Client())


def test_ireland_videos(client, mock_s3_ireland):
    response = client.get('/ireland')
    assert response.status_code == 200
    html = response.data.decode('utf-8') # Decode bytes to string
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-One.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Two.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Three.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Four.mov"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-One-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Two-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Three-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Four-still-001.jpg"' in html


def test_japan_videos(client, mock_s3_japan):
    response = client.get('/japan')
    assert response.status_code == 200
    html = response.data.decode('utf-8') # Decode bytes to string
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Japan-2019-Osaka.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Japan-2019.mov"' in html


def test_uk_videos(client, mock_s3_uk):
    response = client.get('/uk')
    assert response.status_code == 200
    html = response.data.decode('utf-8') # Decode bytes to string
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Five.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Six.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Seven.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Eight.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-England-Day-Nine.mov"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Five-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Six-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Seven-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Eight-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-England-Day-Nine-still-001.jpg"' in html


def test_get_video_data_invalid_prefix(mock_s3_ireland):
    from app.main import get_video_data
    videos = get_video_data(prefix='invalid/')  # Non-matching prefix
    assert len(videos) == 0  # Hits line 78


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


def test_flask_installed():
    result = subprocess.run(["pip", "show", "flask"], capture_output=True, text=True)
    assert "Name: Flask" in result.stdout


def test_pytest_installed():
    result = subprocess.run(["pip", "show", "pytest"], capture_output=True, text=True)
    assert "Name: pytest" in result.stdout


def test_cloudfront_images_accessible():
    """Test that CloudFront image URLs return a 200 status code."""
    image_urls = [
        'https://d1rhrn7ca7di1b.cloudfront.net/images/IMG_3137.jpeg',
        'https://d1rhrn7ca7di1b.cloudfront.net/images/RenderedImage.jpeg',
        'https://d1rhrn7ca7di1b.cloudfront.net/images/IMG_3305-225x300.jpeg'
    ]

    for url in image_urls:
        response = requests.get(url)
        assert response.status_code == 200, f"Failed to access {url}: {response.status_code}"
