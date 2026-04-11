import { api } from './api';
import {
	AvatarPresignedUrlResponse,
	UserLoginForm,
	UserRegistrationForm,
	UserEditForm,
	UserProfile,
} from '../../api/types';

export const authApi = api.injectEndpoints({
	endpoints: (build) => ({
		login: build.mutation<void, UserLoginForm>({
			query: (credentials) => ({
				url: '/auth/login',
				method: 'POST',
				body: credentials,
			}),
		}),

		register: build.mutation<void, UserRegistrationForm>({
			query: (userData) => ({
				url: '/auth/register',
				method: 'POST',
				body: userData,
			}),
		}),

		logout: build.mutation<void, void>({
			query: () => ({
				url: '/auth/logout',
				method: 'POST'
			}),
		}),

		getProfile: build.query<UserProfile, void>({
			query: () => '/auth/profile',
			providesTags: ['Profile'],
		}),

		editProfile: build.mutation<UserProfile, UserEditForm>({
			query: (userData) => ({
				url: '/auth/profile',
				method: 'PATCH',
				body: userData,
			}),
			invalidatesTags: ['Profile'],
		}),

		getAvatarPresignedUrl: build.query<AvatarPresignedUrlResponse, string>({
			query: (contentType) => ({
				url: '/auth/profile/avatar/presigned-url',
				params: { content_type: contentType },
			}),
		}),

		updateAvatar: build.mutation<UserProfile, { key: string }>({
			query: (data) => ({
				url: '/auth/profile/avatar',
				method: 'PATCH',
				body: data,
			}),
			invalidatesTags: ['Profile'],
		}),
	}),
});

export const {
	useLoginMutation,
	useRegisterMutation,
	useLogoutMutation,
	useGetProfileQuery,
	useEditProfileMutation,
	useLazyGetAvatarPresignedUrlQuery,
	useUpdateAvatarMutation,
} = authApi;
