import { FC, useState } from 'react';
import { useGetVideosByAuthorQuery } from '@/store/api/video.api';
import { useAppSelector } from '@/hooks/storeHooks';
import { VideoCard } from '@/components/VideoCard/VideoCard';
import { UploadVideoForm } from '@/components/UploadVideoForm/UploadVideoForm';
import { Button } from '@/ui/Button/Button';
import cls from './MyVideos.module.scss';

export const MyVideos: FC = () => {
	const [showUploadForm, setShowUploadForm] = useState(false);
	const currentUser = useAppSelector((state) => state.auth.user);
	const { data: videos, isLoading, refetch } = useGetVideosByAuthorQuery(currentUser?.username || '', {
		skip: !currentUser?.username
	});

	const handleUploadSuccess = () => {
		setShowUploadForm(false);
		refetch();
	};

	if (isLoading) {
		return (
			<div className={cls.myVideosPage}>
				<h2 className={cls.title}>Мои видео</h2>
				<p className={cls.loading}>Загрузка...</p>
			</div>
		);
	}

	return (
		<div className={cls.myVideosPage}>
			<div className={cls.header}>
				<h2 className={cls.title}>Мои видео</h2>
				<Button
					text={showUploadForm ? 'Отменить' : 'Загрузить видео'}
					onClick={() => setShowUploadForm(!showUploadForm)}
					primary={!showUploadForm}
				/>
			</div>

			{showUploadForm && (
				<div className={cls.uploadFormWrapper}>
					<UploadVideoForm onSuccess={handleUploadSuccess} />
				</div>
			)}

			<div className={cls.videoGrid}>
				{videos && videos.length > 0 ? (
					videos.map((video) => (
						<VideoCard
							key={video.id}
							id={video.id}
							title={video.title}
							description={video.description}
							author={`${video.author.first_name} ${video.author.last_name}`}
							authorUsername={video.author.username}
							preview_url={video.preview_url}
							views={video.views}
							created_at={video.created_at}
							isOwner={true}
							onVideoUpdate={refetch}
						/>
					))
				) : (
					<p className={cls.emptyMessage}>У вас пока нет загруженных видео</p>
				)}
			</div>
		</div>
	);
}; 