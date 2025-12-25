from flask.testing import FlaskClient
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


def test_index_route_renders_images(client: FlaskClient):
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
    assert b'href="/greece"' in response.data
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
def mock_s3_ireland(monkeypatch: pytest.MonkeyPatch):
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
def mock_s3_japan(monkeypatch: pytest.MonkeyPatch):
    class MockS3Client:
        def list_objects_v2(self, Bucket, Prefix):
            if Prefix == 'videos/':
                return {
                    'Contents': [
                        {'Key': 'videos/Japan-2019-Osaka.mov'},
                        {'Key': 'videos/Japan-2019.mov'},
                        {'Key': 'videos/Tokyo.mov'}
                    ]
                }
            elif Prefix == 'stills/':
                return {
                    'Contents': [
                        {'Key': 'stills/Japan-2019-Osaka-still-001.jpg'},
                        {'Key': 'stills/Japan-2019-still-001.jpg'},
                        {'Key': 'stills/Tokyo.mov'}
                    ]
                }
            return {'Contents': []}
    monkeypatch.setattr('app.main.s3_client', MockS3Client())


@pytest.fixture
def mock_s3_uk(monkeypatch: pytest.MonkeyPatch):
    class MockS3Client:
        def list_objects_v2(self, Bucket, Prefix):
            if Prefix == 'videos/':
                return {
                    'Contents': [
                        {'Key': 'videos/Ireland-Scotland-Day-Five.mov'},
                        {'Key': 'videos/Ireland-Scotland-Day-Six.mov'},
                        {'Key': 'videos/Ireland-Scotland-Day-Seven.mov'},
                        {'Key': 'videos/Ireland-Scotland-Day-Eight.mov'},
                        {'Key': 'videos/Ireland-Scotland-England-Day-Nine.mov'},
                        {'Key': 'videos/Edinburgh-Day-Ten.mov'},
                        {'Key': 'videos/Edinburgh-Day-Eleven.mp4'}
                    ]
                }
            elif Prefix == 'stills/':
                return {
                    'Contents': [
                        {'Key': 'stills/Ireland-Scotland-Day-Five-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-Day-Six-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-Day-Seven-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-Day-Eight-still-001.jpg'},
                        {'Key': 'stills/Ireland-Scotland-England-Day-Nine-still-001.jpg'},
                        {'Key': 'stills/Edinburgh-Day-Ten-still-001.jpg'},
                        {'Key': 'stills/Edinburgh-Day-Eleven-still-001.jpg'}
                    ]
                }
            return {'Contents': []}
    monkeypatch.setattr('app.main.s3_client', MockS3Client())


@pytest.fixture
def mock_s3_greece(monkeypatch: pytest.MonkeyPatch):
    class MockS3Client:
        def list_objects_v2(self, Bucket, Prefix):
            if Prefix == 'videos/':
                return {
                    'Contents': [
                        {'Key': 'videos/Greece-Day-1.mov'}
                    ]
                }
            elif Prefix == 'stills/':
                return {
                    'Contents': [
                        {'Key': 'stills/Greece-Day-1-still-001.jpg'}
                    ]
                }
            return {'Contents': []}
    monkeypatch.setattr('app.main.s3_client', MockS3Client())


def test_ireland_videos(client: FlaskClient, mock_s3_ireland: None):
    response = client.get('/ireland')
    assert response.status_code == 200
    html = response.data.decode('utf-8')  # Decode bytes to string
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-One.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Two.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Three.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Four.mov"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-One-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Two-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Three-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Four-still-001.jpg"' in html


def test_japan_videos(client: FlaskClient, mock_s3_japan: None):
    response = client.get('/japan')
    assert response.status_code == 200
    html = response.data.decode('utf-8')  # Decode bytes to string
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Japan-2019-Osaka.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Japan-2019.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Tokyo.mov"' in html


def test_uk_videos(client: FlaskClient, mock_s3_uk: None):
    response = client.get('/uk')
    assert response.status_code == 200
    html = response.data.decode('utf-8')  # Decode bytes to string
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Five.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Six.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Seven.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-Day-Eight.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Ireland-Scotland-England-Day-Nine.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Edinburgh-Day-Ten.mov"' in html
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Edinburgh-Day-Eleven.mp4"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Five-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Six-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Seven-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-Day-Eight-still-001.jpg"' in html
    poster_url = "https://d1rhrn7ca7di1b.cloudfront.net/stills/Ireland-Scotland-England-Day-Nine-still-001.jpg"
    assert f'poster="{poster_url}"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Edinburgh-Day-Ten-still-001.jpg"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Edinburgh-Day-Eleven-still-001.jpg"' in html


def test_greece_videos(client: FlaskClient, mock_s3_greece: None):
    response = client.get('/greece')
    assert response.status_code == 200
    html = response.data.decode('utf-8')  # Decode bytes to string
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Greece-Day-1.mov"' in html


@pytest.fixture
def mock_s3_bahamas(monkeypatch: pytest.MonkeyPatch):
    class MockS3Client:
        def list_objects_v2(self, Bucket, Prefix):
            if Prefix == 'videos/':
                return {
                    'Contents': [
                        {'Key': 'videos/Bahamas 2025.mp4'}
                    ]
                }
            elif Prefix == 'stills/':
                return {
                    'Contents': [
                        {'Key': 'stills/Bahamas 2025-still-001.jpg'}
                    ]
                }
            return {'Contents': []}
    monkeypatch.setattr('app.main.s3_client', MockS3Client())


def test_bahamas_page():
    client = app.test_client()
    response = client.get('/bahamas')
    assert response.status_code == 200
    assert b"BAHAMAS" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


def test_bahamas_page_content():
    """Test that the Bahamas page has correct content."""
    client = app.test_client()
    response = client.get('/bahamas')
    html = response.data.decode('utf-8')
    assert 'Fourth of July' in html
    assert 'Cape Canaveral' in html
    assert 'Nassau' in html
    assert "Sydney's parents" in html


def test_bahamas_videos(client: FlaskClient, mock_s3_bahamas: None):
    response = client.get('/bahamas')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert '<source src="https://d1rhrn7ca7di1b.cloudfront.net/videos/Bahamas 2025.mp4"' in html
    assert 'poster="https://d1rhrn7ca7di1b.cloudfront.net/stills/Bahamas 2025-still-001.jpg"' in html


def test_home_page_bahamas_tile():
    """Test that the home page has the Bahamas tile."""
    client = app.test_client()
    response = client.get('/')
    html = response.data.decode('utf-8')
    assert 'href="/bahamas"' in html
    assert 'BAHAMAS' in html


def test_home_page_our_travels_tile():
    """Test that the home page has the Our Travels tile."""
    client = app.test_client()
    response = client.get('/')
    html = response.data.decode('utf-8')
    assert 'href="/maps"' in html
    assert 'OUR TRAVELS' in html


def test_header_has_bahamas_link():
    """Test that the header navigation includes Bahamas."""
    client = app.test_client()
    response = client.get('/')
    html = response.data.decode('utf-8')
    assert '<a href="/bahamas">Bahamas</a>' in html


def test_get_video_data_invalid_prefix(mock_s3_ireland: None):
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
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


def test_maps_page_title_and_header():
    """Test that the maps page has correct title and header."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert '<title>Travel Map</title>' in html
    assert "Where We've Been" in html
    assert 'A family journey across the globe' in html


def test_maps_page_filter_tabs():
    """Test that all filter tabs are present."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'data-filter="all"' in html
    assert 'data-filter="jay"' in html
    assert 'data-filter="sydney"' in html
    assert 'data-filter="reagan"' in html
    assert 'data-filter="taylor"' in html
    assert 'All Trips' in html


def test_maps_page_family_cards():
    """Test that all family member cards are present."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    # Check for family cards
    assert 'data-member="jay"' in html
    assert 'data-member="sydney"' in html
    assert 'data-member="reagan"' in html
    assert 'data-member="taylor"' in html
    # Check for avatars
    assert 'class="avatar">J</div>' in html
    assert 'class="avatar">S</div>' in html
    assert 'class="avatar">R</div>' in html
    assert 'class="avatar">T</div>' in html


def test_maps_page_jay_destinations():
    """Test Jay's destinations are displayed correctly."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert '14 destinations visited' in html
    # Family trips
    assert 'Greece' in html
    assert 'Bahamas' in html
    assert 'Ireland' in html
    assert 'Northern Ireland' in html
    assert 'Scotland' in html
    assert 'England' in html
    assert 'Japan' in html
    assert 'Turkey' in html
    assert 'Mexico' in html
    # Solo trips
    assert 'Germany' in html
    assert 'Iraq' in html
    assert 'Taiwan' in html
    assert 'Costa Rica' in html
    assert 'Portugal' in html


def test_maps_page_sydney_destinations():
    """Test Sydney's destinations are displayed correctly."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert '9 destinations visited' in html


def test_maps_page_reagan_taylor_destinations():
    """Test Reagan and Taylor's destinations are displayed correctly."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert '7 destinations visited' in html


def test_maps_page_globe_container():
    """Test that the 3D globe container is present."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'class="globe-container"' in html
    assert 'id="globe"' in html
    assert 'Our Global Footprint' in html


def test_maps_page_globe_script():
    """Test that Globe.gl script is included."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'https://unpkg.com/globe.gl' in html
    assert 'Globe()' in html


def test_maps_page_destinations_data():
    """Test that destinations data is present in JavaScript."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    # Check destination coordinates
    assert "name: 'Japan'" in html
    assert "name: 'Ireland'" in html
    assert "name: 'Greece'" in html
    assert "name: 'Turkey'" in html
    assert "name: 'Bahamas'" in html
    assert "name: 'Mexico'" in html
    assert "name: 'Germany'" in html
    assert "name: 'Iraq'" in html
    assert "name: 'Taiwan'" in html
    assert "name: 'Costa Rica'" in html
    assert "name: 'Portugal'" in html
    assert "name: 'Northern Ireland'" in html
    assert "name: 'Scotland'" in html
    assert "name: 'England'" in html


def test_maps_page_stats_section():
    """Test that stats section displays correct numbers."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'class="stats-row"' in html
    assert '>14</div>' in html  # Countries
    assert '>3</div>' in html   # Continents
    assert '>4</div>' in html   # Family Trips
    assert 'Countries' in html
    assert 'Continents' in html
    assert 'Family Trips' in html


def test_maps_page_timeline_section():
    """Test that timeline section is present with header."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'class="timeline-section"' in html
    assert 'Our Journey Through Time' in html
    assert 'class="timeline"' in html


def test_maps_page_timeline_upcoming_trip():
    """Test that upcoming Mediterranean cruise is displayed."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'Mediterranean Cruise' in html
    assert 'Upcoming' in html
    assert '2026' in html
    assert 'MSC cruise departing from Rome' in html
    assert 'Spain, France, and Italy' in html


def test_maps_page_timeline_bahamas():
    """Test Bahamas trip entry in timeline."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'Bahamas Cruise' in html
    assert 'Fourth of July cruise' in html
    assert "Sydney's parents" in html
    assert 'Cape Canaveral' in html
    assert 'Nassau' in html


def test_maps_page_timeline_greece():
    """Test Greece trip entry in timeline."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'Greece Adventure' in html
    assert 'href="/greece"' in html
    assert 'Acropolis' in html
    assert 'Resilient Lady' in html
    assert 'Rhodes' in html
    assert 'Ephesus' in html
    assert 'Santorini' in html
    assert 'Crete' in html


def test_maps_page_timeline_ireland_uk():
    """Test Ireland & UK trip entry in timeline."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'href="/ireland"' in html
    assert 'href="/uk"' in html
    assert '2023' in html
    assert 'Eleven days' in html
    assert 'Emerald Isle' in html
    assert 'Dublin' in html
    assert 'Blarney Castle' in html
    assert 'Cliffs of Moher' in html
    assert 'Giants Causeway' in html
    assert 'Glasgow' in html
    assert 'Loch Ness' in html
    assert 'Edinburgh' in html
    assert 'Semple' in html
    assert 'Caerlaverock' in html


def test_maps_page_timeline_japan():
    """Test Japan trip entry in timeline."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'href="/japan"' in html
    assert '2019' in html
    assert 'Osaka' in html
    assert 'Bullet Train' in html
    assert 'Nagoya' in html
    assert 'Tokyo' in html
    assert '2020 Olympics' in html


def test_maps_page_timeline_taiwan():
    """Test Taiwan trip entry in timeline."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'Taiwan' in html
    assert '2017' in html
    assert 'program meetings' in html
    assert 'customer project' in html


def test_maps_page_timeline_portugal():
    """Test Portugal trip entry in timeline."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'Portugal' in html
    assert '2016' in html
    assert 'NATO Seasparrow' in html
    assert 'Missile Program' in html


def test_maps_page_timeline_iraq():
    """Test Iraq trip entry in timeline."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'Iraq' in html
    assert '2010' in html
    assert 'Six month deployment' in html
    assert 'Uncle Sam' in html
    assert 'Ops Officer' in html
    assert 'DCMA' in html


def test_maps_page_timeline_mexico():
    """Test Mexico trip entry in timeline."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert '1999' in html
    assert 'Tijuana' in html
    assert 'San Diego' in html
    assert 'Navy' in html


def test_maps_page_timeline_costa_rica():
    """Test Costa Rica trip entry in timeline."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert '1996' in html
    assert 'Costa Rica' in html
    assert 'Graduation surf trip' in html
    assert 'Jaco' in html
    assert 'Pacific coast' in html


def test_maps_page_color_scheme():
    """Test that family color scheme is applied."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    # Jay - Yellow
    assert '#F4D03F' in html
    # Sydney - Pink
    assert '#FF6B9D' in html
    # Reagan - Coral
    assert '#FF8A65' in html
    # Taylor - Purple
    assert '#9B59B6' in html


def test_maps_page_filter_javascript():
    """Test that filter JavaScript functionality is present."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'filterTabs.forEach' in html
    assert 'updateGlobePoints' in html
    assert 'getFilteredDestinations' in html
    assert "dataset.filter" in html


def test_maps_page_globe_configuration():
    """Test Globe.gl configuration options."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'globeImageUrl' in html
    assert 'earth-blue-marble.jpg' in html
    assert 'bumpImageUrl' in html
    assert 'pointsData' in html
    assert 'autoRotate' in html
    assert 'pointOfView' in html
    assert 'onPointClick' in html


def test_maps_page_travelers_data_attributes():
    """Test that timeline items have correct data-travelers attributes."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    # Family trips should have all travelers
    assert 'data-travelers="jay sydney reagan taylor"' in html
    # Solo trips should only have jay
    assert 'data-travelers="jay"' in html


def test_maps_page_mini_badges():
    """Test that mini badges are present in timeline."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert 'class="mini-badge jay">J</span>' in html
    assert 'class="mini-badge sydney">S</span>' in html
    assert 'class="mini-badge reagan">R</span>' in html
    assert 'class="mini-badge taylor">T</span>' in html


def test_maps_page_responsive_styles():
    """Test that responsive media query styles are present."""
    client = app.test_client()
    response = client.get('/maps')
    html = response.data.decode('utf-8')
    assert '@media (max-width: 900px)' in html


def test_greece_page():
    client = app.test_client()
    response = client.get('/greece')
    assert response.status_code == 200
    assert b"Greece" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data


def test_flask_installed():
    result = subprocess.run(["pip3", "show", "flask"], capture_output=True, text=True)
    assert "Name: Flask" in result.stdout


def test_pytest_installed():
    result = subprocess.run(["pip3", "show", "pytest"], capture_output=True, text=True)
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
