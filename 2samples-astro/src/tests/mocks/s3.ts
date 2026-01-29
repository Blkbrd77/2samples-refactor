import { vi } from 'vitest';

export const createMockS3Client = (videoContents: { Key: string }[], stillContents: { Key: string }[]) => {
  return {
    send: vi.fn().mockImplementation((command: { input?: { Prefix?: string } }) => {
      const prefix = command.input?.Prefix || '';
      if (prefix.includes('stills')) {
        return Promise.resolve({ Contents: stillContents });
      }
      return Promise.resolve({ Contents: videoContents });
    }),
  };
};

export const mockVideoData = [
  { Key: 'videos/Japan-2019-Osaka.mp4' },
  { Key: 'videos/Japan-2019.mp4' },
  { Key: 'videos/Tokyo.mov' },
];

export const mockStillData = [
  { Key: 'stills/Japan-2019-Osaka-still-001.jpg' },
  { Key: 'stills/Japan-2019-Osaka-still-002.jpg' },
  { Key: 'stills/Japan-2019-still-001.jpg' },
  { Key: 'stills/Tokyo-still-002.jpg' },
];

export const emptyMockData: { Key: string }[] = [];
