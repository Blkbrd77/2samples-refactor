from flask import Flask 

app = Flask(__name__)

@app.route('/')
def home ():
    return "<h1>Welcome to 2samples Travels!</h1><p>Stories from the road, coming soon.<a href=\"/stories\">Check out our stories!</a></p>"

@app.route('/stories')
def stories():
    return "<h1>Travel Stories</h1><p>Coming soon-tales from our adventures!<p>"

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


