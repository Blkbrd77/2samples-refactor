from app.main import app
import subprocess

def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"TRAVELS" in response.data  # Header title
    assert b'href="/japan2019"' in response.data  # Japan link
    assert b'href="/ireland"' in response.data    # Ireland link
    assert b'href="/uk"' in response.data         # UK link
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data     # Nav bar
    assert b'class="tile"' in response.data       # Tiles

def test_japan2019_page():
    client = app.test_client()
    response = client.get('/japan2019')
    assert response.status_code == 200
    assert b"JAPAN 2019" in response.data         # Page title
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data     # Nav bar

def test_ireland_page():
    client = app.test_client()
    response = client.get('/ireland')
    assert response.status_code == 200
    assert b"REPUBLIC OF IRELAND" in response.data  # Page title
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data     # Nav bar

def test_uk_page():
    client = app.test_client()
    response = client.get('/uk')
    assert response.status_code == 200
    assert b"UNITED KINGDOM" in response.data     # Page title
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data     # Nav bar

def test_irelanduk_page():
    client = app.test_client()
    response = client.get('/irelanduk')
    assert response.status_code == 200
    assert b"Ireland and UK Travels" in response.data  # Page title
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data     # Nav bar

def test_stories_page():
    client = app.test_client()
    response = client.get('/stories')
    assert response.status_code == 200
    assert b"Travel Stories" in response.data     # Page title
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'href="/stories/1"' in response.data  # Story link
    assert b'class="header"' in response.data     # Nav bar

def test_story_page():
    client = app.test_client()
    response = client.get('/stories/1')
    assert response.status_code == 200
    assert b"A Desert Adventure" in response.data  # Story title
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data     # Nav bar

def test_blog_page():
    client = app.test_client()
    response = client.get('/blog')
    assert response.status_code == 200
    assert b"Blog" in response.data               # Page title
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data     # Nav bar

def test_maps_page():
    client = app.test_client()
    response = client.get('/maps')
    assert response.status_code == 200
    assert b"Maps" in response.data               # Page title
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data     # Nav bar

def test_privacy_page():
    client = app.test_client()
    response = client.get('/privacy')
    assert response.status_code == 200
    assert b"Privacy Policy" in response.data     # Page title
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data
    assert b'class="header"' in response.data     # Nav bar

def test_flask_installed():
    result = subprocess.run(["pip", "show", "flask"], capture_output=True, text=True)
    assert "Name: Flask" in result.stdout

def test_pytest_installed():
    result = subprocess.run(["pip", "show", "pytest"], capture_output=True, text=True)
    assert "Name: pytest" in result.stdout