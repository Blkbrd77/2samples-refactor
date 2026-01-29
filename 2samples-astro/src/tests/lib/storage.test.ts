import { describe, it, expect } from 'vitest';
import { processVideoData, CLOUDFRONT_URL } from '../../lib/storage';

// Test data
const mockVideoContents = [
  { Key: 'videos/Japan-2019-Osaka.mp4' },
  { Key: 'videos/Japan-2019.mp4' },
  { Key: 'videos/Tokyo.mov' },
];

const mockStillContents = [
  { Key: 'stills/Japan-2019-Osaka-still-001.jpg' },
  { Key: 'stills/Japan-2019-Osaka-still-002.jpg' },
  { Key: 'stills/Japan-2019-still-001.jpg' },
  { Key: 'stills/Tokyo-still-002.jpg' },
];

describe('Storage - processVideoData', () => {
  it('should return an array of videos', () => {
    const videos = processVideoData(mockVideoContents, mockStillContents);
    expect(Array.isArray(videos)).toBe(true);
    expect(videos.length).toBeGreaterThan(0);
  });

  it('should return videos with url, name, and still properties', () => {
    const videos = processVideoData(mockVideoContents, mockStillContents);

    videos.forEach((video) => {
      expect(video).toHaveProperty('url');
      expect(video).toHaveProperty('name');
      expect(video).toHaveProperty('still');
    });
  });

  it('should construct CloudFront URLs for videos', () => {
    const videos = processVideoData(mockVideoContents, mockStillContents);

    videos.forEach((video) => {
      expect(video.url).toContain(CLOUDFRONT_URL);
      expect(video.url).toMatch(/\.(mp4|mov)$/i);
    });
  });

  it('should extract video name from key', () => {
    const videos = processVideoData(mockVideoContents, mockStillContents);

    const names = videos.map((v) => v.name);
    expect(names).toContain('Japan-2019-Osaka');
    expect(names).toContain('Japan-2019');
    expect(names).toContain('Tokyo');
  });

  it('should prefer still-001.jpg when available', () => {
    const videos = processVideoData(mockVideoContents, mockStillContents);

    const osakaVideo = videos.find((v) => v.name === 'Japan-2019-Osaka');
    expect(osakaVideo?.still).toContain('still-001.jpg');
  });

  it('should fall back to first still if no still-001', () => {
    const videos = processVideoData(mockVideoContents, mockStillContents);

    const tokyoVideo = videos.find((v) => v.name === 'Tokyo');
    expect(tokyoVideo?.still).toContain('Tokyo-still-002.jpg');
  });

  it('should handle empty data gracefully', () => {
    const videos = processVideoData([], []);

    expect(Array.isArray(videos)).toBe(true);
    expect(videos.length).toBe(0);
  });

  it('should not include duplicate video names', () => {
    const duplicateVideos = [
      { Key: 'videos/Test.mp4' },
      { Key: 'videos/Test.mov' },
    ];
    const videos = processVideoData(duplicateVideos, []);

    const names = videos.map((v) => v.name);
    const uniqueNames = [...new Set(names)];
    expect(names.length).toBe(uniqueNames.length);
  });

  it('should handle videos with no matching stills', () => {
    const videos = processVideoData(mockVideoContents, []);

    videos.forEach((video) => {
      expect(video.still).toBeNull();
    });
  });
});
