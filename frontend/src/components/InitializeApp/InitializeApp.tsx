import { FC, useEffect } from 'react';
import { useGetProfileQuery } from '../../store/api/auth.api';
import { useAppDispatch } from '@/hooks/storeHooks';
import { authSlice } from '@/store/auth/auth.slice';
interface InitializeAppProps {
  children: React.ReactNode;
}

export const InitializeApp: FC<InitializeAppProps> = ({ children }) => {
  const dispatch = useAppDispatch();
  const { data, isLoading, isSuccess } = useGetProfileQuery(undefined);
  if(isSuccess){
    dispatch(authSlice.actions.setUser(data));
  }
  if (isLoading) {
    return null; // или можно показать loader
  }

  return <>{children}</>;
}; 