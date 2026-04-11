import { FC } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGetMySubscriptionsQuery, useUnsubscribeMutation } from '@/store/api/subscription.api';
import { useGetVideosByAuthorQuery } from '@/store/api/video.api';
import { Button } from '@/ui/Button/Button';
import cls from './Subscriptions.module.scss';

export const Subsriptions: FC = () => {
	const { data: subscriptions, isLoading, error } = useGetMySubscriptionsQuery();
	const [unsubscribe] = useUnsubscribeMutation();
	const navigate = useNavigate();

	if (isLoading) {
		return <div className={cls.subscriptionsPage}>
			<h2 className={cls.title}>Загрузка подписок...</h2>
		</div>;
	}

	if (error) {
		console.error('Ошибка при загрузке подписок:', error);
		return <div className={cls.subscriptionsPage}>
			<h2 className={cls.title}>Не удалось загрузить подписки</h2>
			<p className={cls.errorMessage}>Произошла ошибка при загрузке ваших подписок. Пожалуйста, попробуйте позже.</p>
		</div>;
	}

	if (!subscriptions || subscriptions.length === 0) {
		return <div className={cls.subscriptionsPage}>
			<h2 className={cls.title}>Подписки</h2>
			<p className={cls.emptyMessage}>У вас пока нет подписок</p>
		</div>;
	}

	const handleUnsubscribe = async (username: string) => {
		try {
			await unsubscribe(username);
		} catch (error) {
			console.error('Failed to unsubscribe:', error);
		}
	};

	return (
		<div className={cls.subscriptionsPage}>
			<h2 className={cls.title}>Ваши подписки</h2>
			<div className={cls.grid}>
				{subscriptions.map((subscription) => (
					<ChannelCard
						key={subscription.username}
						subscription={subscription}
						onUnsubscribe={handleUnsubscribe}
						onChannelClick={() => navigate(`/channel/${subscription.username}`)}
						navigate={navigate}
					/>
				))}
			</div>
		</div>
	);
};

interface ChannelCardProps {
	subscription: any;
	onUnsubscribe: (username: string) => void;
	onChannelClick: () => void;
	navigate: (path: string) => void;
}

const ChannelCard: FC<ChannelCardProps> = ({ subscription, onUnsubscribe, onChannelClick, navigate }) => {
	const { data: videos } = useGetVideosByAuthorQuery(subscription.username);
	const latestVideos = videos?.slice(0, 3) || [];

	return (
		<div className={cls.channelCard}>
			<div className={cls.channelInfo} onClick={onChannelClick}>
				<img
					src={subscription.avatar || `https://ui-avatars.com/api/?name=${subscription.username}`}
					alt={subscription.username}
					className={cls.avatar}
				/>
				<div className={cls.info}>
					<h3 className={cls.name}>
						{subscription.first_name} {subscription.last_name}
						<span className={cls.username}>@{subscription.username}</span>
					</h3>
					<p className={cls.stats}>
						{subscription.total_subscribers} подписчиков
					</p>
				</div>
			</div>

			<div className={cls.videos}>
				<h4 className={cls.videosTitle}>Последние видео</h4>
				<div className={cls.videoGrid}>
					{latestVideos.map((video) => (
						<div
							key={video.id}
							className={cls.videoPreview}
							onClick={() => navigate(`/video/${video.id}`)}
						>
							{video.preview_url ? (
								<img src={video.preview_url} alt={video.title} />
							) : (
								<div className={cls.placeholder} />
							)}
							<span className={cls.videoTitle}>{video.title}</span>
							<span className={cls.views}>{video.views} просмотров</span>
						</div>
					))}
					{latestVideos.length === 0 && (
						<p className={cls.noVideos}>Нет загруженных видео</p>
					)}
				</div>
			</div>

			<Button
				text="Отписаться"
				onClick={() => onUnsubscribe(subscription.username)}
				size="s"
				primary={false}
			/>
		</div>
	);
};
