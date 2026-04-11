# Video Hosting Frontend

This is a React-based frontend for a video hosting platform with HLS support.

## Features

- Complete API client for all backend endpoints
- HLS video playback support
- TypeScript support
- Authentication handling
- Video upload and management
- Comments system
- Like/dislike functionality
- Subscription system

## Installation

```bash
npm install
```

## Usage

### API Client

Initialize the API client:

```typescript
import { ApiClient } from './api/client';

const api = new ApiClient('http://your-api-base-url');

// After login, set the JWT token
api.setToken(jwtToken);
```

Example usage:

```typescript
// Authentication
const login = async () => {
  const response = await api.login({
    email: 'user@example.com',
    password: 'password'
  });
  api.setToken(response.acces_token);
};

// Upload video
const uploadVideo = async (file: File) => {
  await api.uploadVideo(file, 'My Video Title', 'Video description');
};

// Get video details
const getVideo = async (videoId: number) => {
  const video = await api.getVideo(videoId);
  console.log(video);
};
```

### Video Player

The VideoPlayer component supports both HLS (.m3u8) and regular video sources:

```typescript
import { VideoPlayer } from './components/VideoPlayer';

// In your component:
const MyComponent = () => {
  return (
    <VideoPlayer
      src="https://example.com/video.m3u8"
      poster="https://example.com/thumbnail.jpg"
      onTimeUpdate={(currentTime) => console.log('Current time:', currentTime)}
      onEnded={() => console.log('Video ended')}
      className="my-video-player"
    />
  );
};
```

## API Endpoints

The API client supports all endpoints from the backend:

### Authentication
- Login
- Register
- Logout
- Get/Edit Profile

### Videos
- Upload video
- Get video details
- Edit video
- Delete video
- Get video list
- Search videos
- Get videos by author
- Process old video
- View history

### Comments
- Get comments
- Create comment
- Edit comment
- Delete comment

### Likes
- Set like/dislike

### Subscriptions
- Subscribe to channel
- Unsubscribe from channel
- Get subscriptions
- Get all channels

## Development

```bash
npm start
```

This will start the development server at http://localhost:3000.

## Building for Production

```bash
npm run build
```

This will create an optimized production build in the `build` directory.

## Notes

- The video player uses hls.js for HLS playback with fallback to native HLS support for Safari
- All API responses are typed for better development experience
- The API client handles authentication via JWT tokens
- Error handling is implemented for HLS playback
