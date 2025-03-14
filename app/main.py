from flask import Flask, render_template
import boto3


app = Flask(__name__)
s3_client = boto3.client('s3')
BUCKET_NAME = '2samples-static-assets-211125453069'
CLOUDFRONT_URL = 'https://d1rhrn7ca7di1b.cloudfront.net'


# Define the placeholder image URL globally
placeholder_image = "https://d1rhrn7ca7di1b.cloudfront.net/images/comingSoon.jpg"


def get_video_data(prefix='videos/'):
    video_response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    videos = [
        {
            'url': f"{CLOUDFRONT_URL}/{obj['Key']}",
            'name': obj['Key'].split('/')[-1].split('.')[0]
        }
        for obj in video_response.get('Contents', [])
        if obj['Key'].lower().endswith(('.mp4', '.mov'))
    ]

    still_response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='stills/')
    stills = {obj['Key'].split('-still-')[0].split('/')[-1]: f"{CLOUDFRONT_URL}/{obj['Key']}"
              for obj in still_response.get('Contents', [])}

    for video in videos:
        video['still'] = stills.get(video['name'], None)

    return videos


@app.route('/')
def home():
    return render_template('index.html', placeholder_image=placeholder_image)


@app.route('/japan')
def japan():
    return render_template('japan.html', placeholder_image=placeholder_image)


@app.route('/ireland')
def ireland():
    videos = get_video_data()
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
