import { createRoot } from 'react-dom/client';
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom';

import { MainPage } from '@/pages/MainPage/MainPage';
import { ProtectionRoute } from '@/components/ProtectionRoute/ProtectionRoute';
import { Reg } from '@/pages/AuthPage/Reg/Reg';
import { Login } from '@/pages/AuthPage/Login/Login';
import { MainLayout } from '@/components/MainLayout/MainLayout';
import { Subsriptions } from '@/pages/Subscriptions/Subscriptions';
import { VideoPage } from '@/pages/VideoPage/VideoPage';
import { SearchPage } from '@/pages/SearchPage/SearchPage';
import { ChannelPage } from '@/pages/ChannelPage/ChannelPage';
import { History } from '@/pages/History/History';
import { MyVideos } from '@/pages/MyVideos/MyVideos';
import { Provider } from 'react-redux';
import { store } from '@/store/store';
import { InitializeApp } from '@/components/InitializeApp/InitializeApp';
import '@/styles/global.scss';
import '@/styles/variables.scss';
import { ProfilePage } from '@/pages/ProfilePage/ProfilePage';

const routes = createBrowserRouter([
	{
		path: '/',
		element: <ProtectionRoute />,
		children: [
			{
				element: <MainLayout />,
				children: [
					{
						index: true,
						element: <MainPage />
					},
					{
						path: 'channel/:username',
						element: <ChannelPage />
					},
					{
						path: 'video/:id',
						element: <VideoPage />
					},
					{
						path: 'subscriptions',
						element: <Subsriptions />
					},
					{
						path: 'search',
						element: <SearchPage />
					},
					{
						path: 'history',
						element: <History />
					},
					{
						path: 'myVideos',
						element: <MyVideos />
					},
					{
						path: 'profile',
						element: <ProfilePage />
					}
				]
			}
		]
	},
	{
		path: 'auth',
		children: [
			{
				index: true,
				element: <Navigate to="login" replace />
			},
			{
				path: 'reg',
				element: <Reg />
			},
			{
				path: 'login',
				element: <Login />
			}
		]
	}
]);

const root = createRoot(document.getElementById('root')!);

root.render(
	<Provider store={store}>
		<InitializeApp>
			<RouterProvider router={routes} />
		</InitializeApp>
	</Provider>
);
