# app.py
from main import app as main  # Import the 'app' instance from main.py as 'main'

if __name__ == "__main__":
    main.run(host='0.0.0.0', port=8000)
