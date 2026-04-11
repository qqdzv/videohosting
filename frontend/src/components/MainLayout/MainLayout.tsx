import { FC } from 'react';
import cls from './MainLayout.module.scss';
import { Header } from '@/components/Header/Header';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { useGetMySubscriptionsQuery } from '@/store/api/subscription.api';
import { useNotificationsWS } from '@/hooks/useNotificationsWS';
import { notificationsApi } from '@/api/notifications.api';
import { useAppDispatch } from '@/hooks/storeHooks';

export const MainLayout: FC = () => {
	const location = useLocation();
	const dispatch = useAppDispatch();
	const { data: subscriptions = [] } = useGetMySubscriptionsQuery();
	useNotificationsWS(() => dispatch(notificationsApi.util.invalidateTags(['Notification'])));

	const isActiveRoute = (path: string) => {
		return location.pathname === path;
	};

	return (
		<main className={cls.mainLayout}>
			<Header />
			<div className={cls.content}>
				<nav className={cls.nav}>
					<Link to="/" className={`${cls.navItem} ${isActiveRoute('/') ? cls.active : ''}`}>
						<img src={`/icons/home${isActiveRoute('/') ? '_active' : ''}.svg`} alt="home" />
						<span>Домой</span>
					</Link>
					<Link to="/myVideos" className={`${cls.navItem} ${isActiveRoute('/myVideos') ? cls.active : ''}`}>
						<img src={`/icons/video${isActiveRoute('/myVideos') ? '_active' : ''}.svg`} alt="my videos" />
						<span>Мои видео</span>
					</Link>
					<Link to="/history" className={`${cls.navItem} ${isActiveRoute('/history') ? cls.active : ''}`}>
						<img src={`/icons/history${isActiveRoute('/history') ? '_active' : ''}.svg`} alt="history" />
						<span>История</span>
					</Link>
					<Link to="/subscriptions" className={`${cls.navItem} ${isActiveRoute('/subscriptions') ? cls.active : ''}`}>
						<img src={`/icons/subs${isActiveRoute('/subscriptions') ? '_active' : ''}.svg`} alt="subscriptions" />
						<span>Подписки</span>
					</Link>

					{subscriptions.length > 0 && (
						<div className={cls.subscriptionsList}>
							<div className={cls.subscriptionsTitle}>Подписки</div>
							{subscriptions.map((subscription) => (
								<Link
									key={subscription.username}
									to={`/channel/${subscription.username}`}
									className={`${cls.navItem} ${cls.subscriptionItem}`}
								>
									<img
										src={subscription.avatar || `https://ui-avatars.com/api/?name=${subscription.username}`}
										alt={subscription.username}
										className={cls.avatar}
									/>
									<span>{subscription.username}</span>
								</Link>
							))}
						</div>
					)}
				</nav>
				<div className={cls.mainContent}>
					<Outlet />
				</div>
			</div>
		</main>
	);
};
