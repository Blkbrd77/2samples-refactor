from flask import Flask, render_template

app = Flask(__name__)

# Base template function (optional, for shared layout)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/japan2019')
def japan2019():
    return render_template('japan2019.html')

@app.route('/ireland')
def ireland():
    return render_template('ireland.html')

@app.route('/uk')
def uk():
    return render_template('uk.html')

@app.route('/irelanduk')
def irelanduk():
    return render_template('irelanduk.html')

@app.route('/stories')
def stories():
    return render_template('stories.html')

@app.route('/stories/1')
def story_1():
    return render_template('story1.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/maps')
def maps():
    return render_template('maps.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)