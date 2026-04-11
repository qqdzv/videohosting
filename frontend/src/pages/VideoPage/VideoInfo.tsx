import React, { useState } from 'react';
import { GetVideo } from '../../api/types';
import { useSetLikeMutation } from '../../store/api/like.api';
import { useSubscribeMutation, useUnsubscribeMutation, useIsSubscribedQuery } from '../../store/api/subscription.api';
import { useAppSelector } from '@/hooks/storeHooks';
import styles from './VideoInfo.module.scss';

interface VideoInfoProps {
	video: GetVideo;
}

export const VideoInfo: React.FC<VideoInfoProps> = ({ video }) => {
	const [setLike] = useSetLikeMutation();
	const [subscribe, { isLoading: isSubscribing }] = useSubscribeMutation();
	const [unsubscribe, { isLoading: isUnsubscribing }] = useUnsubscribeMutation();
	const isLoadingSubscription = isSubscribing || isUnsubscribing;
	const currentUser = useAppSelector((state) => state.auth.user);
	const { data: isSubscribed } = useIsSubscribedQuery(video.author.username || '');
	const isOwnVideo = currentUser?.username === video.author.username;
	const [showShareMessage, setShowShareMessage] = useState(false);

	const handleLike = async (isLike: boolean) => {
		try {
			await setLike({
				videoId: video.id,
				data: { reaction: isLike ? 'like' : 'dislike' }
			});
		} catch (error) {
			console.error('Failed to set reaction:', error);
		}
	};

	const handleSubscribe = async () => {
		try {
			if (isSubscribed?.success) {
				await unsubscribe(video.author.username);
			} else {
				await subscribe(video.author?.username);
			}
		} catch (error) {
			console.error('Failed to change subscription:', error);
		}
	};

	const handleShare = async () => {
		try {
			await navigator.clipboard.writeText(window.location.href);
			setShowShareMessage(true);
			setTimeout(() => setShowShareMessage(false), 2000);
		} catch (error) {
			console.error('Failed to copy link:', error);
		}
	};

	return (
		<div className={styles.container}>
			<h1 className={styles.title}>{video.title}</h1>

			<div className={styles.metadata}>
				<div className={styles.authorInfo}>
					<img
						src={video.author.avatar || `https://ui-avatars.com/api/?name=${video.author.username}`}
						alt={`${video.author.first_name} ${video.author.last_name}`}
						className={styles.avatar}
					/>
					<div className={styles.authorDetails}>
						<div className={styles.authorName}>
							<span>
								{video.author.first_name} {video.author.last_name}
							</span>
							<span className={styles.username}>@{video.author.username}</span>
						</div>
						<div className={styles.subscriberCount}>{video.author.total_subscribers} подписчиков</div>
					</div>
					{!isOwnVideo && (
						<button
							className={`${styles.subscribeButton} ${isSubscribed?.success ? styles.subscribed : ''} ${isLoadingSubscription ? styles.loading : ''}`}
							onClick={handleSubscribe}
							disabled={isLoadingSubscription}
						>
							{isLoadingSubscription ? <span className={styles.spinner} /> : (isSubscribed?.success ? 'Отписаться' : 'Подписаться')}
						</button>
					)}
				</div>

				<div className={styles.stats}>
					<span>{video.views} просмотров</span>
					<div className={styles.actions}>
						<div className={styles.reactions}>
							<button
								className={`${styles.reactionButton} ${video.reaction === 'like' ? styles.active : ''}`}
								onClick={() => handleLike(true)}
							>
								<span>👍</span>
								<span>{video.likes}</span>
							</button>
							<button
								className={`${styles.reactionButton} ${video.reaction === 'dislike' ? styles.active : ''}`}
								onClick={() => handleLike(false)}
							>
								<span>👎</span>
								<span>{video.dislikes}</span>
							</button>
						</div>
						<button className={styles.shareButton} onClick={handleShare}>
							<img src="/icons/share.svg" alt="share" />
							<span>Поделиться</span>
						</button>
						{showShareMessage && (
							<div className={styles.shareMessage}>
								Ссылка скопирована!
							</div>
						)}
					</div>
				</div>
			</div>

			<div className={styles.description}>
				<p>{video.description}</p>
				<span className={styles.date}>{new Date(video.created_at || '').toLocaleDateString()}</span>
			</div>
		</div>
	);
};
