import { FC, useEffect, useState } from 'react';
import { SearchBar } from '@/ui/SearchBar/SearchBar';
import cls from './Header.module.scss';
import { AccountWidget } from '../AccountWidget/AccountWidget';
import { NotificationsWidget } from '../NotificationsWidget/NotificationsWidget';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAppSelector } from '@/hooks/storeHooks';

export const Header: FC = () => {
	const navigate = useNavigate();
	const [searchParams] = useSearchParams();
	const [searchValue, setSearchValue] = useState(decodeURIComponent(searchParams.get('q') || ''));
	const user = useAppSelector((state) => state.auth.user);

	const handleSearch = (e: React.FormEvent) => {
		e.preventDefault();
		if (searchValue.trim()) {
			const encodedQuery = encodeURIComponent(searchValue.trim());
			navigate(`/search?q=${encodedQuery}`);
		}
	};
	useEffect(() => {
		setSearchValue(decodeURIComponent(searchParams.get('q') || ''));
	}, [searchParams]);
	return (
		<header className={cls.header}>
			<img src="/logo.svg" alt="logo" className={cls.logo} onClick={() => navigate('/')} />
			{user && (
				<div className={cls.right}>
					<form onSubmit={handleSearch}>
						<SearchBar 
							value={searchValue} 
							onChange={(e) => setSearchValue(e.target.value)}
							onSubmit={handleSearch}
						/>
					</form>
					<NotificationsWidget />
					<AccountWidget
						username={user?.username || user?.first_name + ' ' + user?.last_name}
						subscribers={user?.total_subscribers}
						avatar={user?.avatar}
					/>
				</div>
			)}
		</header>
	);
};
