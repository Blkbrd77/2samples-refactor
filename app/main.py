from flask import Flask, render_template

app = Flask(__name__)

# Define the placeholder image URL globally
placeholder_image = "https://d1rhrn7ca7di1b.cloudfront.net/images/comingSoon.jpg"


@app.route('/')
def home():
    return render_template('index.html', placeholder_image=placeholder_image)


@app.route('/japan2019')
def japan2019():
    return render_template('japan2019.html', placeholder_image=placeholder_image)


@app.route('/ireland')
def ireland():
    return render_template('ireland.html', placeholder_image=placeholder_image)


@app.route('/uk')
def uk():
    return render_template('uk.html', placeholder_image=placeholder_image)


@app.route('/blog')
def blog():
    return render_template('blog.html', placeholder_image=placeholder_image)


@app.route('/maps')
def maps():
    return render_template('maps.html', placeholder_image=placeholder_image)


@app.route('/privacy')
def privacy():
    return render_template('privacy.html', placeholder_image=placeholder_image)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
