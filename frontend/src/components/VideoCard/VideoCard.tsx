import { FC, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDeleteVideoMutation } from '@/store/api/video.api';
import { formatViewsCount, formatRelativeDate } from '@/utils/format';
import { EditVideoModal } from '@/components/EditVideoModal/EditVideoModal';
import { DropdownMenu } from '@/components/DropdownMenu/DropdownMenu';
import cls from './VideoCard.module.scss';

interface VideoCardProps {
	preview_url?: string;
	author: string;
	title: string;
	description?: string;
	id: number;
	authorUsername: string;
	views: number;
	created_at: string;
	isSubscribed?: boolean;
	isOwner?: boolean;
	onVideoUpdate?: () => void;
}

export const VideoCard: FC<VideoCardProps> = ({ 
	preview_url, 
	id, 
	authorUsername, 
	views, 
	created_at, 
	isSubscribed,
	isOwner,
	description,
	onVideoUpdate,
	...props 
}) => {
	const navigate = useNavigate();
	const [showEditModal, setShowEditModal] = useState(false);
	const [deleteVideo] = useDeleteVideoMutation();

	const handleAuthorClick = (e: React.MouseEvent) => {
		e.stopPropagation();
		navigate(`/channel/${authorUsername}`);
	};

	const handleEdit = () => {
		setShowEditModal(true);
	};

	const handleDelete = async () => {
		if (window.confirm('Вы уверены, что хотите удалить это видео?')) {
			try {
				await deleteVideo(id).unwrap();
				onVideoUpdate?.();
			} catch (error) {
				console.error('Failed to delete video:', error);
			}
		}
	};

	const menuItems = [
		{ label: 'Изменить', onClick: handleEdit },
		{ label: 'Удалить', onClick: handleDelete, danger: true }
	];

	return (
		<>
			<article className={cls.videoCard} onClick={() => navigate(`/video/${id}`)}>
				<div className={cls.preview}>
					{preview_url ? <img src={preview_url} alt="preview" /> : <div className={cls.blackBox} />}
				</div>
				<div className={cls.info}>
					<div className={cls.titleRow}>
						<span className={cls.name}>{props.title}</span>
						{isOwner && (
							<div className={cls.actions} onClick={e => e.stopPropagation()}>
								<DropdownMenu items={menuItems} />
							</div>
						)}
					</div>
					<div className={cls.details}>
						<p className={`${cls.author} ${isSubscribed ? cls.subscribed : ''}`} onClick={handleAuthorClick}>
							{props.author}
						</p>
						<div className={cls.stats}>
							<span>{formatViewsCount(Number(views))} просмотров</span>
							<span>·</span>
							<span>{formatRelativeDate(created_at)}</span>
						</div>
					</div>
				</div>
			</article>

			{showEditModal && (
				<EditVideoModal
					videoId={id}
					initialTitle={props.title}
					initialDescription={description || ''}
					onClose={() => setShowEditModal(false)}
					onSuccess={() => {
						setShowEditModal(false);
						onVideoUpdate?.();
					}}
				/>
			)}
		</>
	);
};
