import { FC } from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { useAppSelector } from '@/hooks/storeHooks';

export const ProtectionRoute: FC = () => {
	const isAuthenticated = useAppSelector(state => state.auth.isAuthenticated)
	if (!isAuthenticated) {
		return <Navigate to='/auth' />
	}
	return <Outlet />
}
