import { FC } from 'react';
import { useNavigate } from 'react-router-dom';
import cls from './AccountWidget.module.scss';

export const AccountWidget: FC<{ username: string; subscribers: number; avatar?: string }> = ({ username, subscribers, avatar }) => {
	const navigate = useNavigate();

	return (
		<article className={cls.accountWidget} onClick={() => navigate('/profile')}>
			<img src={avatar || `https://ui-avatars.com/api/?name=${username}`} alt="Profile" className={cls.avatar} />
			<section className={cls.info}>
				<span>{username}</span>
				<p>Подписчиков: {subscribers}</p>
			</section>
		</article>
	);
};
