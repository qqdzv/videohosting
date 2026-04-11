import { FC, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useGetVideosByAuthorQuery } from '@/store/api/video.api';
import { useSubscribeMutation, useUnsubscribeMutation, useIsSubscribedQuery } from '@/store/api/subscription.api';
import { useAppSelector } from '@/hooks/storeHooks';
import { VideoCard } from '@/components/VideoCard/VideoCard';
import { Button } from '@/ui/Button/Button';
import cls from './ChannelPage.module.scss';

export const ChannelPage: FC = () => {
	const { username } = useParams<{ username: string }>();
	const [activeTab, setActiveTab] = useState<'videos' | 'about'>('videos');
	const { data: videos, isLoading: videosLoading } = useGetVideosByAuthorQuery(username || '');
	const { data: isSubscribed } = useIsSubscribedQuery(username || '');
	const [subscribe, { isLoading: isSubscribing }] = useSubscribeMutation();
	const [unsubscribe, { isLoading: isUnsubscribing }] = useUnsubscribeMutation();
	const currentUser = useAppSelector((state) => state.auth.user);
	console.log(isSubscribed);
	if (!username) return <div className={cls.error}>Канал не найден</div>;
	if (videosLoading) return <div className={cls.loading}>Загрузка...</div>;
	const channelInfo = videos?.[0]?.author;
	const isOwnChannel = currentUser?.username === username;
	const totalVideos = videos?.length || 0;

	const handleSubscribe = async () => {
		try {
			if (isSubscribed?.success) {
				await unsubscribe(username);
			} else {
				await subscribe(username);
			}
		} catch (error) {
			console.error('Failed to change subscription:', error);
		}
	};

	return (
		<div className={cls.channelPage}>
			<div className={cls.header}>
				<div className={cls.channelInfo}>
					<img
						src={channelInfo?.avatar || `https://ui-avatars.com/api/?name=${channelInfo?.username}`}
						alt={channelInfo?.username}
						className={cls.avatar}
					/>
					<div className={cls.info}>
						<h1 className={cls.name}>
							{channelInfo?.first_name} {channelInfo?.last_name}
							<span className={cls.username}>@{channelInfo?.username}</span>
						</h1>
						<div className={cls.stats}>
							<span>{channelInfo?.total_subscribers} подписчиков</span>
							<span>{totalVideos} видео</span>
						</div>
					</div>
					{!isOwnChannel && (
						<Button
							text={isSubscribed?.success ? 'Отписаться' : 'Подписаться'}
							onClick={handleSubscribe}
							primary={!isSubscribed?.success}
							subscribed={!!isSubscribed?.success}
							loading={isSubscribing || isUnsubscribing}
							size="s"
						/>
					)}
				</div>
				<div className={cls.tabs}>
					<button className={`${cls.tab} ${activeTab === 'videos' ? cls.active : ''}`} onClick={() => setActiveTab('videos')}>
						ВИДЕО
					</button>
					<button className={`${cls.tab} ${activeTab === 'about' ? cls.active : ''}`} onClick={() => setActiveTab('about')}>
						О КАНАЛЕ
					</button>
				</div>
			</div>

			<div className={cls.content}>
				{activeTab === 'videos' ? (
					<div className={cls.videos}>
						{videos?.map((video) => (
							<VideoCard
								key={video.id}
								id={video.id}
								title={video.title}
								author={`${video.author.first_name} ${video.author.last_name}`}
								authorUsername={video.author.username}
								preview_url={video.preview_url}
								views={video.views}
								created_at={video.created_at}
								isSubscribed={isSubscribed?.success}
							/>
						))}
						{videos?.length === 0 && <div className={cls.empty}>На этом канале пока нет видео</div>}
					</div>
				) : (
					<div className={cls.about}>
						<div className={cls.section}>
							<h3>Описание</h3>
							<p>Канал пользователя {channelInfo?.username}</p>
						</div>
						<div className={cls.section}>
							<h3>Статистика</h3>
							<div className={cls.statsList}>
								<div className={cls.statItem}>
									<span className={cls.label}>Подписчиков</span>
									<span className={cls.value}>{channelInfo?.total_subscribers || 0}</span>
								</div>
								<div className={cls.statItem}>
									<span className={cls.label}>Видео</span>
									<span className={cls.value}>{totalVideos}</span>
								</div>
							</div>
						</div>
					</div>
				)}
			</div>
		</div>
	);
};
