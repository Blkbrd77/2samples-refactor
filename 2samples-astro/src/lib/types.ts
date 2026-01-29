export interface Video {
  url: string;
  name: string;
  still: string | null;
}

export interface S3Object {
  Key?: string;
}

export interface ListObjectsResponse {
  Contents?: S3Object[];
}
