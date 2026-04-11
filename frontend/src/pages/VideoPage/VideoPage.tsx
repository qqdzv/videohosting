import React, { useEffect, useRef } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { VideoPlayer } from '../../components/VideoPlayer/VideoPlayer';
import { Comments } from './Comments';
import { VideoInfo } from './VideoInfo';
import { useGetVideoQuery, useAddVideoViewMutation } from '../../store/api/video.api';
import styles from './VideoPage.module.scss';

type VideoParams = {
	id: string | undefined;
}

export const VideoPage: React.FC = () => {
	const { id } = useParams<'id'>();
	const location = useLocation();
	const videoId = Number(id);
	const [addVideoView] = useAddVideoViewMutation();
	const viewAdded = useRef(false);
	
	useEffect(() => {
		console.log('Current route params:', { id, location: location.pathname });
		console.log('Parsed video ID:', videoId);
		
		// Reset the view flag when the video ID changes
		viewAdded.current = false;
	}, [id, location, videoId]);

	if (!id) {
		console.error('Идентификатор видео не указан');
		return <div className={styles.container}>Идентификатор видео не указан</div>;
	}

	if (isNaN(videoId)) {
		console.error('Неверный формат идентификатора видео:', id);
		return <div className={styles.container}>Неверный формат идентификатора видео: {id}</div>;
	}

	const { data: video, isLoading, error } = useGetVideoQuery(videoId);

	const handleVideoPlay = () => {
		if (!viewAdded.current && !isNaN(videoId)) {
			addVideoView(videoId).catch(error => {
				console.error('Не удалось увеличить количество просмотров:', error);
			});
			viewAdded.current = true;
		}
	};

	if (isLoading) {
		return <div className={styles.container}>Загрузка...</div>;
	}

	if (error) {
		console.error('Ошибка при загрузке видео:', error);
		return <div className={styles.container}>Ошибка при загрузке видео</div>;
	}

	if (!video) {
		return <div className={styles.container}>Видео не найдено</div>;
	}

	return (
		<div className={styles.container}>
			<div className={styles.videoWrapper}>
				<VideoPlayer 
					src={video.video_hls || ''} 
					poster={video.preview_url}
					onPlay={handleVideoPlay}
				/>
			</div>

			<VideoInfo video={video} />

			<div className={styles.commentsSection}>
				<Comments videoId={video.id} />
			</div>
		</div>
	);
};
