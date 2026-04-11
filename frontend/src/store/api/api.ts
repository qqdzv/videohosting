import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { BaseQueryFn, FetchArgs, FetchBaseQueryError } from '@reduxjs/toolkit/query'
import { actions } from '@/store/auth/auth.slice';

const baseQuery = fetchBaseQuery({
	baseUrl: import.meta.env.VITE_API_URL,
	credentials: 'include',
});

const baseQueryWithReauth: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> = async (
	args,
	api,
	extraOptions,
) => {
	const result = await baseQuery(args, api, extraOptions);

	if (result.error?.status === 401 && !window.location.pathname.startsWith('/auth')) {
		api.dispatch(actions.logout());
		window.location.href = '/auth/login';
	}

	return result;
};

export const api = createApi({
	reducerPath: 'api',
	tagTypes: ['Video', 'Comment', 'Profile', 'Subscription'],
	baseQuery: baseQueryWithReauth,
	endpoints: () => ({})
})
