from app.main import app

def test_home_page():
    client = app.test_client() #Flask's built-in way to simulate requests
    response = client.get('/') #Simulate visiting the homepage
    assert response.status_code == 200 #check it loads successfully
    assert b"Welcome" in response.data #Check "Welcome" is in the page
    assert b'href="/stories"' in response.data # Check for the link
    assert b"<style>" in response.data # Check for CSS Styling

def test_stories_page():
    client = app.test_client()
    response = client.get('stories')
    assert response.status_code == 200
    assert b"Travel Stories" in response.data