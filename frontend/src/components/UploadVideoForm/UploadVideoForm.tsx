import { FC, useState, useRef } from 'react';
import { useUploadVideoMutation } from '@/store/api/video.api';
import { Button } from '@/ui/Button/Button';
import { BaseInput } from '@/ui/BaseInput/BaseInput';
import cls from './UploadVideoForm.module.scss';

export const UploadVideoForm: FC<{ onSuccess?: () => void }> = ({ onSuccess }) => {
	const [uploadVideo, { isLoading }] = useUploadVideoMutation();
	const fileInputRef = useRef<HTMLInputElement>(null);
	const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [title, setTitle] = useState('');
	const [description, setDescription] = useState('');
	const [error, setError] = useState<string | null>(null);

	const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0];
		if (file) {
			if (file.type.startsWith('video/')) {
				setSelectedFile(file);
				setError(null);
			} else {
				setError('Пожалуйста, выберите видео файл');
				setSelectedFile(null);
			}
		}
	};

	const handleSubmit = async (e?: React.FormEvent) => {
		if (e) {
			e.preventDefault();
		}
		if (!selectedFile) {
			setError('Пожалуйста, выберите файл');
			return;
		}
		if (!title.trim()) {
			setError('Пожалуйста, введите название');
			return;
		}

		try {
			await uploadVideo({
				file: selectedFile,
				title: title.trim(),
				description: description.trim()
			}).unwrap();

			// Reset form
			setSelectedFile(null);
			setTitle('');
			setDescription('');
			setError(null);
			if (fileInputRef.current) {
				fileInputRef.current.value = '';
			}
			onSuccess?.();
		} catch (err) {
			setError('Произошла ошибка при загрузке видео');
			console.error('Upload error:', err);
		}
	};

	return (
		<form className={cls.uploadForm} onSubmit={handleSubmit}>
			<h3 className={cls.title}>Загрузить новое видео</h3>
			
			<div className={cls.fileInput}>
				<input
					type="file"
					accept="video/*"
					onChange={handleFileSelect}
					ref={fileInputRef}
					id="video-file"
				/>
				<label htmlFor="video-file" className={cls.fileLabel}>
					{selectedFile ? selectedFile.name : 'Выберите видео файл'}
				</label>
			</div>

			<BaseInput
				type="text"
				value={title}
				onChange={(e) => setTitle(e.target.value)}
				placeholder="Название видео"
				label="Название"
			/>

			<BaseInput
				type="text"
				value={description}
				onChange={(e) => setDescription(e.target.value)}
				placeholder="Описание видео"
				label="Описание"
			/>

			{error && <p className={cls.error}>{error}</p>}

			<Button
				text={isLoading ? 'Загрузка...' : 'Загрузить видео'}
				onClick={() => handleSubmit()}
				type="submit"
				disabled={isLoading}
				primary
			/>
		</form>
	);
}; 