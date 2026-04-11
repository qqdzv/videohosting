import React, { useEffect, useRef } from 'react';
import Hls from 'hls.js';

interface VideoPlayerProps {
  src: string;
  poster?: string;
  onTimeUpdate?: (currentTime: number) => void;
  onEnded?: () => void;
  onPlay?: () => void;
  className?: string;
}

export const VideoPlayer: React.FC<VideoPlayerProps> = ({
  src,
  poster,
  onTimeUpdate,
  onEnded,
  onPlay,
  className,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const hlsRef = useRef<Hls | null>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const initializeHls = () => {
      if (hlsRef.current) {
        hlsRef.current.destroy();
      }

      const hls = new Hls({
        enableWorker: true,
        lowLatencyMode: true,
      });

      hls.attachMedia(video);
      hls.on(Hls.Events.MEDIA_ATTACHED, () => {
        hls.loadSource(src);
      });

      hls.on(Hls.Events.ERROR, (event, data) => {
        if (data.fatal) {
          switch (data.type) {
            case Hls.ErrorTypes.NETWORK_ERROR:
              console.error('Ошибка сети, пытаемся восстановить...');
              hls.startLoad();
              break;
            case Hls.ErrorTypes.MEDIA_ERROR:
              console.error('Ошибка медиа, пытаемся восстановить...');
              hls.recoverMediaError();
              break;
            default:
              console.error('Неустранимая ошибка');
              hls.destroy();
              break;
          }
        }
      });

      hlsRef.current = hls;
    };

    if (src.includes('.m3u8')) {
      if (Hls.isSupported()) {
        initializeHls();
      } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = src;
      }
    } else {
      video.src = src;
    }

    return () => {
      if (hlsRef.current) {
        hlsRef.current.destroy();
      }
    };
  }, [src]);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      onTimeUpdate?.(video.currentTime);
    };

    const handleEnded = () => {
      onEnded?.();
    };

    const handlePlay = () => {
      onPlay?.();
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('ended', handleEnded);
    video.addEventListener('play', handlePlay);

    return () => {
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('ended', handleEnded);
      video.removeEventListener('play', handlePlay);
    };
  }, [onTimeUpdate, onEnded, onPlay]);

  return (
    <video
      ref={videoRef}
      className={className}
      poster={poster}
      controls
      playsInline
      style={{ width: '100%', height: '100%' }}
    />
  );
}; 