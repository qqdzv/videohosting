import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '@/hooks/storeHooks';
import {
	useEditProfileMutation,
	useLazyGetAvatarPresignedUrlQuery,
	useLogoutMutation,
	useUpdateAvatarMutation,
} from '@/store/api/auth.api';
import { actions } from '@/store/auth/auth.slice';

const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_AVATAR_SIZE = 5 * 1024 * 1024; // 5 МБ
import { BaseInput } from '@/ui/BaseInput/BaseInput';
import { validateEmail, validateRequired } from '@/utils/validation';
import { ValidationErrors } from '@/types/auth.types';
import styles from './ProfilePage.module.scss';
import fields from './ProfileFieles';

export const ProfilePage = () => {
	const navigate = useNavigate();
	const dispatch = useAppDispatch();
	const user = useAppSelector((state) => state.auth.user);
	const [editProfile] = useEditProfileMutation();
	const [logout] = useLogoutMutation();
	const [getPresignedUrl] = useLazyGetAvatarPresignedUrlQuery();
	const [updateAvatar] = useUpdateAvatarMutation();

	const fileInputRef = useRef<HTMLInputElement>(null);
	const [isUploadingAvatar, setIsUploadingAvatar] = useState(false);
	const [avatarError, setAvatarError] = useState<string | null>(null);

	const [isEditing, setIsEditing] = useState(false);
	const [formData, setFormData] = useState({
		first_name: user?.first_name || '',
		last_name: user?.last_name || '',
		email: user?.email || '',
		username: user?.username || ''
	});
	const [errors, setErrors] = useState<ValidationErrors>({});
	const [submitAttempted, setSubmitAttempted] = useState(false);
	const [generalError, setGeneralError] = useState<string | null>(null);

	const validateForm = (): boolean => {
		const newErrors: ValidationErrors = {};

		// Validate required fields
		Object.keys(formData).forEach((key) => {
			const value = formData[key as keyof typeof formData];
			const error = validateRequired(value);
			if (error) {
				newErrors[key as keyof typeof formData] = error;
			}
		});

		// Email validation
		if (!newErrors.email) {
			const emailError = validateEmail(formData.email);
			if (emailError) newErrors.email = emailError;
		}

		setErrors(newErrors);
		return Object.keys(newErrors).length === 0;
	};

	const handleChange = (key: keyof typeof formData, value: string) => {
		setFormData(prev => ({ ...prev, [key]: value }));
		if (submitAttempted) {
			setErrors(prev => {
				const newErrors = { ...prev };
				delete newErrors[key];
				return newErrors;
			});
		}
		setGeneralError(null);
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setSubmitAttempted(true);
		setGeneralError(null);
		
		if (!validateForm()) {
			return;
		}

		try {
			await editProfile(formData).unwrap();
			setIsEditing(false);
			setErrors({});
			setSubmitAttempted(false);
		} catch (err: any) {
			console.log('Error from backend:', err);
			
			if (err.data && typeof err.data === 'object') {
				const serverErrors: ValidationErrors = {};
				
				if (Array.isArray(err.data)) {
					setGeneralError(err.data[0]);
				} else {
					Object.entries(err.data).forEach(([key, value]) => {
						if (Array.isArray(value)) {
							serverErrors[key as keyof typeof formData] = value[0];
						} else if (typeof value === 'string') {
							serverErrors[key as keyof typeof formData] = value as string;
						} else if (typeof value === 'object' && value !== null) {
							serverErrors[key as keyof typeof formData] = (value as any).message || JSON.stringify(value);
						}
					});
					
					if (Object.keys(serverErrors).length > 0) {
						console.log('Setting field errors:', serverErrors);
						setErrors(serverErrors);
					} else {
						setGeneralError(
							typeof err.data === 'string' 
								? err.data 
								: 'Произошла ошибка при обновлении профиля'
						);
					}
				}
			} else if (err.status === 401) {
				setGeneralError('Необходима повторная авторизация');
				dispatch(actions.logout());
				navigate('/auth/login');
			} else if (err.status === 403) {
				setGeneralError('У вас нет прав для выполнения этого действия');
			} else if (err.status === 422) {
				setGeneralError('Неверный формат данных');
			} else {
				setGeneralError(
					err.data?.message || err.data || 'Произошла ошибка при обновлении профиля'
				);
			}
		}
	};

	const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0];
		if (!file) return;

		setAvatarError(null);

		if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
			setAvatarError('Допустимые форматы: JPEG, PNG, WebP');
			e.target.value = '';
			return;
		}
		if (file.size > MAX_AVATAR_SIZE) {
			setAvatarError('Максимальный размер: 5 МБ');
			e.target.value = '';
			return;
		}

		setIsUploadingAvatar(true);
		try {
			const { presigned_url, key } = await getPresignedUrl(file.type).unwrap();

			await fetch(presigned_url, {
				method: 'PUT',
				body: file,
				headers: { 'Content-Type': file.type },
			});

			const updatedProfile = await updateAvatar({ key }).unwrap();
			dispatch(actions.setUser(updatedProfile));
		} catch {
			setAvatarError('Ошибка при загрузке аватарки');
		} finally {
			setIsUploadingAvatar(false);
			e.target.value = '';
		}
	};

	const handleLogout = async () => {
		try {
			await logout().unwrap();
			dispatch(actions.logout());
			navigate('/auth/login');
		} catch (error) {
			console.error('Logout error:', error);
			setGeneralError('Произошла ошибка при выходе из системы');
		}
	};

	if (!user) return null;

	return (
		<div className={styles.profilePage}>
			<div className={styles.profileContainer}>
				<div className={styles.header}>
					<h1>Профиль</h1>
					<div className={styles.actions}>
						{!isEditing && (
							<button className={styles.editButton} onClick={() => setIsEditing(true)}>
								Редактировать
							</button>
						)}
						<button className={styles.logoutButton} onClick={handleLogout}>
							Выйти
						</button>
					</div>
				</div>

				<div className={styles.profileContent}>
					<div className={styles.avatarSection}>
						<div className={styles.avatarBlock}>
							<img
								src={user.avatar || `https://ui-avatars.com/api/?name=${user.username}`}
								alt="Profile"
								className={styles.avatar}
							/>
							{isEditing && (
								<>
									<button
										type="button"
										className={styles.changeAvatarBtn}
										onClick={() => fileInputRef.current?.click()}
										disabled={isUploadingAvatar}
									>
										{isUploadingAvatar ? (
											<><div className={styles.avatarSpinner} /> Загрузка...</>
										) : (
											'Изменить фото'
										)}
									</button>
									<input
										ref={fileInputRef}
										type="file"
										accept="image/jpeg,image/png,image/webp"
										className={styles.fileInput}
										onChange={handleFileChange}
									/>
								</>
							)}
						</div>
						<div className={styles.userInfo}>
							<h2>{`${user.first_name} ${user.last_name}`}</h2>
							<span className={styles.username}>@{user.username}</span>
							{avatarError && <span className={styles.avatarError}>{avatarError}</span>}
						</div>
					</div>

					{isEditing ? (
						<form onSubmit={handleSubmit} className={styles.form}>
							{fields.map((field) => (
								<BaseInput
									key={field.key}
									label={field.placeholder}
									value={formData[field.key as keyof typeof formData]}
									onChange={(e) => handleChange(field.key as keyof typeof formData, e.target.value)}
									type={field.type}
									placeholder={field.placeholder}
									error={errors[field.key as keyof typeof formData]}
								/>
							))}
							{generalError && (
								<div className={styles.generalError}>{generalError}</div>
							)}
							<div className={styles.formActions}>
								<button type="submit" className={styles.saveButton}>
									Сохранить
								</button>
								<button
									type="button"
									className={styles.cancelButton}
									onClick={() => {
										setIsEditing(false);
										setFormData({
											first_name: user.first_name || '',
											last_name: user.last_name || '',
											email: user.email || '',
											username: user.username || ''
										});
										setErrors({});
										setSubmitAttempted(false);
										setGeneralError(null);
									}}
								>
									Отмена
								</button>
							</div>
						</form>
					) : (
						<div className={styles.details}>
							{fields.map((field) => (
								<div key={field.key} className={styles.detailItem}>
									<span className={styles.label}>{field.label}:</span>
									<span className={styles.value}>{user[field.key as keyof typeof user]}</span>
								</div>
							))}
							{generalError && (
								<div className={styles.generalError}>{generalError}</div>
							)}
						</div>
					)}
				</div>
			</div>
		</div>
	);
};
