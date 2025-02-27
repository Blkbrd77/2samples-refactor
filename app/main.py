from flask import Flask 

app = Flask(__name__)

@app.route('/')
def home ():
    return """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Welcome to 2samples Travels!</h1>
        <p>Stories from the road, coming soon. <a href="/stories">Check out our stories!</a></p>
    </body>
    </html>
    """

@app.route('/stories')
def stories():
  return  """
    <html>
    <head>
       <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Travel Stories</h1>
        <p>Coming soon—tales from our adventures!</p>
    </body>
    </html>
    """

@app.route('/stories/1')
def story_1():
   return """
   <html>
   <head>
        <link rel="stylesheet" href="/static/style.css">
    <head>
    <body>
        <h1>Greek Island Adventure!</h1>
        <p>We cruised the Greek Island Glow with Virgin Voyages!!</p>
        <body>
        </html>
   """
   
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
