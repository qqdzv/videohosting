import { FC } from 'react';
import cls from './MainPage.module.scss';
import { VideoCard } from '@/components/VideoCard/VideoCard';
import { useGetVideosQuery } from '@/store/api/video.api';

export const MainPage: FC = () => {
	const { data: videos } = useGetVideosQuery({});
	return (
		<div className={cls.videoGrid}>
			{videos?.map((video, index) => (
				<VideoCard
					key={index}
					id={video.id}
					title={video.title}
					author={video.author?.username || video.author.first_name + ' ' + video.author.last_name}
					authorUsername={video.author.username}
					preview_url={video.preview_url}
					views={video.views}
					created_at={video.created_at}
				/>
			))}
		</div>
	);
};
