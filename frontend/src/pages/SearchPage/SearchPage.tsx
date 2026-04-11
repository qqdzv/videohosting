import { FC, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useSearchVideosQuery } from '@/store/api/video.api';
import { VideoCard } from '@/components/VideoCard/VideoCard';
import styles from './SearchPage.module.scss';
import { useSearchChannelsQuery } from '@/store/api/subscription.api';

export const SearchPage: FC = () => {
	const [searchParams] = useSearchParams();
	const navigate = useNavigate();
	const [activeTab, setActiveTab] = useState<'all' | 'channels'>('all');
	const query = decodeURIComponent(searchParams.get('q') || '');
	const { data: channels = [], isLoading: isChannelsLoading } = useSearchChannelsQuery(query, {
		skip: !query
	});
	const { data: videos = [], isLoading } = useSearchVideosQuery(query, {
		skip: !query
	});

	if (isLoading) {
		return <div className={styles.loading}>Загрузка...</div>;
	}

	return (
		<div className={styles.container}>
			<h1 className={styles.title}>Результаты поиска для "{query}"</h1>

			<div className={styles.tabs}>
				<button className={`${styles.tab} ${activeTab === 'all' ? styles.active : ''}`} onClick={() => setActiveTab('all')}>
					Все результаты
				</button>
				<button className={`${styles.tab} ${activeTab === 'channels' ? styles.active : ''}`} onClick={() => setActiveTab('channels')}>
					Каналы
				</button>
			</div>

			{activeTab === 'all' ? (
				<div className={styles.results}>
					{videos.length > 0 ? (
						videos.map((video) => (
							<VideoCard
								key={video.id}
								title={video.title}
								id={video.id}
								author={video.author.username || video.author.first_name + ' ' + video.author.last_name}
								authorUsername={video.author.username}
								views={video.views}
								preview_url={video.preview_url}
								created_at={video.created_at}
							/>
						))
					) : (
						<p className={styles.noResults}>Ничего не найдено</p>
					)}
				</div>
			) : (
				<div className={styles.channelResults}>
					{channels.length > 0 ? (
						channels.map((channel) => (
							<div key={channel.username} className={styles.channelCard} onClick={() => navigate(`/channel/${channel.username}`)}>
								<div className={styles.channelInfo}>
									<img
										src={channel.avatar ?? `https://ui-avatars.com/api/?name=${channel.username}`}
										alt={channel.first_name}
										className={styles.channelAvatar}
									/>
									<div className={styles.channelDetails}>
										<h3 className={styles.channelName}>{channel.first_name + ' ' + channel.last_name}</h3>
										<p className={styles.channelUsername}>@{channel.username}</p>
										<div className={styles.channelStats}>
											<span>{channel.total_subscribers} подписчиков</span>
										</div>
									</div>
								</div>
							</div>
						))
					) : (
						<p className={styles.noResults}>Ничего не найдено</p>
					)}
				</div>
			)}
		</div>
	);
};
