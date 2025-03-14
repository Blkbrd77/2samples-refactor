import os
import boto3
import ffmpeg
from pathlib import Path

# AWS S3 setup
s3_client = boto3.client('s3')
BUCKET_NAME = '2samples-static-assets-211125453069'

def download_video_from_s3(video_key, local_path):
    print(f"Attempting to download s3://{BUCKET_NAME}/{video_key} to {local_path}")
    s3_client.download_file(BUCKET_NAME, video_key, local_path)
    print(f"Download complete: {local_path} exists: {os.path.exists(local_path)}")

def generate_stills(video_path, output_dir, video_key, interval=5):
    print(f"Generating stills from {video_path} to {output_dir}")
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        video_name = Path(video_key).stem  # e.g., "Edinburgh-Day-Ten"
        output_pattern = f"{output_dir}/{video_name}-still-%03d.jpg"
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(
            stream,
            output_pattern,
            vf=f"fps=1/{interval}",
            **{'q:v': 2},
            format='image2'
        )
        ffmpeg.run(stream, overwrite_output=True)
        print(f"Stills generated in {output_dir} with pattern {output_pattern}")
    except ffmpeg.Error as e:
        error_msg = e.stderr.decode('utf-8') if e.stderr else "Unknown FFmpeg error"
        print(f"FFmpeg error: {error_msg}")
        raise

def upload_stills_to_s3(output_dir, s3_prefix="stills/", video_key=None):
    print(f"Uploading stills from {output_dir} to s3://{BUCKET_NAME}/{s3_prefix}")
    video_name = Path(video_key).stem if video_key else "unknown"
    for file_path in Path(output_dir).glob(f"{video_name}-still-*.jpg"):
        s3_key = f"{s3_prefix}{file_path.name}"
        print(f"Uploading {file_path} to {s3_key}")
        s3_client.upload_file(
            Filename=str(file_path),
            Bucket=BUCKET_NAME,
            Key=s3_key,
            ExtraArgs={'ContentType': 'image/jpeg'}
        )
        print(f"Uploaded {s3_key}")

def process_all_videos(interval=5):
    # List all videos in the videos/ prefix
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='videos/')
    video_keys = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].lower().endswith(('.mp4', '.mov'))]
    
    local_video_path = "/tmp/video"
    stills_dir = "/tmp/stills"
    
    for video_key in video_keys:
        # Use a unique local path to avoid overwriting (append video name)
        local_video_path = f"/tmp/{Path(video_key).name}"
        download_video_from_s3(video_key, local_video_path)
        generate_stills(local_video_path, stills_dir, video_key, interval)
        upload_stills_to_s3(stills_dir, video_key=video_key)
        os.remove(local_video_path)
        for file in Path(stills_dir).glob("*.jpg"):
            os.remove(file)

if __name__ == "__main__":
    process_all_videos(interval=5)