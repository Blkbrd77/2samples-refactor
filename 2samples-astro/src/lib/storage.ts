import { S3Client, ListObjectsV2Command } from '@aws-sdk/client-s3';
import type { Video, S3Object } from './types';

export const BUCKET_NAME = import.meta.env.S3_BUCKET_NAME || '2samples-static-assets-211125453069';
export const CLOUDFRONT_URL = import.meta.env.CLOUDFRONT_URL || 'https://d1rhrn7ca7di1b.cloudfront.net';

// Create default S3 client
export const createS3Client = () => {
  return new S3Client({
    region: import.meta.env.AWS_REGION || 'us-east-1',
  });
};

/**
 * Pure function to process video and still data into Video objects.
 * This is easily testable without mocking S3.
 */
export function processVideoData(
  videoContents: S3Object[],
  stillContents: S3Object[]
): Video[] {
  const seenNames = new Set<string>();
  const videos: Video[] = [];

  // Process videos
  for (const obj of videoContents) {
    if (!obj.Key) continue;

    const key = obj.Key;
    const fileName = key.split('/').pop() || '';
    const name = fileName.split('.')[0];

    if (key.toLowerCase().match(/\.(mp4|mov)$/) && !seenNames.has(name)) {
      seenNames.add(name);
      videos.push({
        url: `${CLOUDFRONT_URL}/${key}`,
        name,
        still: null,
      });
    }
  }

  // Group all stills by video name
  const allStills: Record<string, string[]> = {};

  for (const obj of stillContents) {
    if (!obj.Key) continue;

    const key = obj.Key;
    const fileName = key.split('/').pop() || '';
    const videoName = fileName.split('-still-')[0];
    const stillUrl = `${CLOUDFRONT_URL}/${key}`;

    if (!allStills[videoName]) {
      allStills[videoName] = [];
    }
    allStills[videoName].push(stillUrl);
  }

  // Assign stills to videos, preferring still-001
  for (const video of videos) {
    const videoStills = allStills[video.name] || [];
    const preferredStill = videoStills.find((url) => url.endsWith('still-001.jpg'));
    video.still = preferredStill || videoStills[0] || null;
  }

  return videos;
}

/**
 * Fetch video data from S3 and process it.
 */
export async function getVideoData(prefix: string = 'videos/'): Promise<Video[]> {
  const client = createS3Client();

  // Get videos
  const videoCommand = new ListObjectsV2Command({
    Bucket: BUCKET_NAME,
    Prefix: prefix,
  });
  const videoResponse = await client.send(videoCommand);

  // Get stills
  const stillCommand = new ListObjectsV2Command({
    Bucket: BUCKET_NAME,
    Prefix: 'stills/',
  });
  const stillResponse = await client.send(stillCommand);

  return processVideoData(
    videoResponse.Contents || [],
    stillResponse.Contents || []
  );
}
