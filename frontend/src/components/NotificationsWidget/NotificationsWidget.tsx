import { FC, useState, useRef, useEffect } from 'react';
import cls from './NotificationsWidget.module.scss';
import { useGetNotificationsQuery, useMarkAsReadMutation } from '@/api/notifications.api';

const formatTime = (iso: string): string => {
	const diff = Date.now() - new Date(iso).getTime();
	const mins = Math.floor(diff / 60000);
	if (mins < 1) return 'только что';
	if (mins < 60) return `${mins} мин назад`;
	const hours = Math.floor(mins / 60);
	if (hours < 24) return `${hours} ч назад`;
	const days = Math.floor(hours / 24);
	return `${days} д назад`;
};

export const NotificationsWidget: FC = () => {
	const [isOpen, setIsOpen] = useState(false);
	const ref = useRef<HTMLDivElement>(null);
	const { data } = useGetNotificationsQuery();
	const notifications = data?.data ?? [];
	const unreadCount = data?.unread ?? 0;
	const [markAsRead] = useMarkAsReadMutation();

	useEffect(() => {
		const handleClickOutside = (e: MouseEvent) => {
			if (ref.current && !ref.current.contains(e.target as Node)) {
				setIsOpen(false);
			}
		};
		document.addEventListener('mousedown', handleClickOutside);
		return () => document.removeEventListener('mousedown', handleClickOutside);
	}, []);

	const handleNotificationClick = async (id: number, isRead: boolean) => {
		if (!isRead) {
			await markAsRead(id);
		}
	};

	return (
		<div className={cls.wrapper} ref={ref}>
			<button className={cls.bell} onClick={() => setIsOpen((prev) => !prev)} aria-label="Уведомления">
				<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
					<path
						d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6V11c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"
						fill="currentColor"
					/>
				</svg>
				{unreadCount > 0 && <span className={cls.badge}>{unreadCount > 99 ? '99+' : unreadCount}</span>}
			</button>

			{isOpen && (
				<div className={cls.dropdown}>
					<h3 className={cls.title}>Уведомления</h3>
					{notifications.length === 0 ? (
						<p className={cls.empty}>Нет уведомлений</p>
					) : (
						<ul className={cls.list}>
							{notifications.map((n) => (
								<li
									key={n.id}
									className={`${cls.item} ${!n.is_read ? cls.unread : ''}`}
									onClick={() => handleNotificationClick(n.id, n.is_read)}
								>
									<span className={cls.message}>{n.message}</span>
									<span className={cls.time}>{formatTime(n.created_at)}</span>
								</li>
							))}
						</ul>
					)}
				</div>
			)}
		</div>
	);
};
