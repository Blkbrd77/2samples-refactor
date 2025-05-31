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
    seen_names = set()
    videos = []
    for obj in video_response.get('Contents', []):
        name = obj['Key'].split('/')[-1].split('.')[0]
        if obj['Key'].lower().endswith(('.mp4', '.mov')) and name not in seen_names:
            seen_names.add(name)
            videos.append({
                'url': f"{CLOUDFRONT_URL}/{obj['Key']}",
                'name': name
            })
    still_response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='stills/')
    # Group all stills by video name
    all_stills = {}
    for obj in still_response.get('Contents', []):
        video_name = obj['Key'].split('-still-')[0].split('/')[-1]
        still_url = f"{CLOUDFRONT_URL}/{obj['Key']}"
        if video_name not in all_stills:
            all_stills[video_name] = []
        all_stills[video_name].append(still_url)
    print("All stills:", all_stills)
    for video in videos:
        video_stills = all_stills.get(video['name'], [])
        # Find still-001 if available, otherwise take the first one
        preferred_still = next((url for url in video_stills if url.endswith('still-001.jpg')),
                               video_stills[0] if video_stills else None)
        video['still'] = preferred_still
    return videos


@app.route('/')
def home():
    return render_template('index.html', placeholder_image=placeholder_image)


@app.route('/japan')
def japan():
    videos = get_video_data()
    return render_template('japan.html', videos=videos, placeholder_image=placeholder_image)


@app.route('/ireland')
def ireland():
    videos = get_video_data()
    return render_template('ireland.html', videos=videos, placeholder_image=placeholder_image)


@app.route('/uk')
def uk():
    videos = get_video_data()
    return render_template('uk.html', videos=videos, placeholder_image=placeholder_image)


@app.route('/blog')
def blog():
    return render_template('blog.html', placeholder_image=placeholder_image)


@app.route('/maps')
def maps():
    return render_template('maps.html', placeholder_image=placeholder_image)


@app.route('/greece')
def greece():
    videos = get_video_data()
    return render_template('greece.html', videos=videos, placeholder_image=placeholder_image)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # pragma: no cover
