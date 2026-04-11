import { FC, useState } from 'react';
import { useEditVideoMutation } from '@/store/api/video.api';
import { Button } from '@/ui/Button/Button';
import cls from './EditVideoModal.module.scss';
import { BaseInput } from '@/ui/BaseInput/BaseInput';

interface EditVideoModalProps {
	videoId: number;
	initialTitle: string;
	initialDescription: string;
	onClose: () => void;
	onSuccess: () => void;
}

export const EditVideoModal: FC<EditVideoModalProps> = ({ videoId, initialTitle, initialDescription, onClose, onSuccess }) => {
	const [title, setTitle] = useState(initialTitle);
	const [description, setDescription] = useState(initialDescription);
	const [editVideo] = useEditVideoMutation();

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		try {
			await editVideo({
				videoId,
				data: { title, description }
			}).unwrap();
			onSuccess();
			onClose();
		} catch (error) {
			console.error('Failed to update video:', error);
		}
	};

	return (
		<div className={cls.modalOverlay} onClick={onClose}>
			<div className={cls.modal} onClick={(e) => e.stopPropagation()}>
				<h3>Редактировать видео</h3>
				<form onSubmit={handleSubmit} className={cls.form}>
					<BaseInput value={title} onChange={(e) => setTitle(e.target.value)} type="text" placeholder="Введите название" label="Название" />
					<BaseInput
						value={description}
						onChange={(e) => setDescription(e.target.value)}
						type="text"
						placeholder="Введите описание"
						label="Описание"
						multiline
						rows={5}
					/>
					<div className={cls.buttons}>
						<Button type="button" size="s" text="Отмена" onClick={onClose} />
						<Button type="submit" size="s" text="Сохранить" primary onClick={() => handleSubmit} />
					</div>
				</form>
			</div>
		</div>
	);
};
