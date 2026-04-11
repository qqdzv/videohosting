import { FC } from 'react';
import { useGetHistoryQuery } from '@/store/api/video.api';
import { VideoCard } from '@/components/VideoCard/VideoCard';
import cls from './History.module.scss';

export const History: FC = () => {
	const { data: historyVideos, isLoading, error } = useGetHistoryQuery();

	if (isLoading) {
		return (
			<div className={cls.historyPage}>
				<h2 className={cls.title}>Загрузка истории...</h2>
			</div>
		);
	}

	if (error) {
		return (
			<div className={cls.historyPage}>
				<h2 className={cls.title}>История просмотров</h2>
				<p className={cls.errorMessage}>Произошла ошибка при загрузке истории просмотров</p>
			</div>
		);
	}

	if (!historyVideos || historyVideos.length === 0) {
		return (
			<div className={cls.historyPage}>
				<h2 className={cls.title}>История просмотров</h2>
				<p className={cls.emptyMessage}>История просмотров пуста</p>
			</div>
		);
	}

	return (
		<div className={cls.historyPage}>
			<h2 className={cls.title}>История просмотров</h2>
			<div className={cls.videoGrid}>
				{historyVideos.map((video) => (
					<VideoCard
						key={video.id}
						id={video.id}
						title={video.title}
						author={`${video.author.first_name} ${video.author.last_name}`}
						authorUsername={video.author.username}
						preview_url={video.preview_url}
						views={video.views}
						created_at={video.created_at}
					/>
				))}
			</div>
		</div>
	);
}; 