from app.main import app
import subprocess

def test_home_page():
    client = app.test_client() #Flask's built-in way to simulate requests
    response = client.get('/') #Simulate visiting the homepage
    assert response.status_code == 200 #check it loads successfully
    assert b"Welcome" in response.data #Check "Welcome" is in the page
    assert b'href="/stories"' in response.data # Check for the link
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data # Check for external CSS 


def test_stories_page():
    client = app.test_client()
    response = client.get('stories')
    assert response.status_code == 200
    assert b"Travel Stories" in response.data
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data # Check for external CSS
    assert b'href="/stories/1"' in response.data #Check for story link 
    
def test_flask_installed():
    result = subprocess.run(["pip", "show", "flask"], capture_output=True, text=True)
    assert "Name: Flask" in result.stdout

def test_pytest_installed():
    result = subprocess.run(["pip", "show", "pytest"], capture_output=True, text=True)
    assert "Name: pytest" in result.stdout

def test_story_page():
    client = app.test_client()
    response = client.get('/stories/1')
    assert response.status_code == 200
    assert b"Greek Island Adventure" in response.data # Story title
    assert b'<link rel="stylesheet" href="/static/style.css">' in response.data 

