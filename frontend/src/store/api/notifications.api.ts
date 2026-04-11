import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export interface NotificationResponse {
	id: number;
	user_id: number;
	type: string;
	message: string;
	is_read: boolean;
	created_at: string;
}

export interface NotificationsListResponse {
	unread: number;
	data: NotificationResponse[];
}

export const notificationsApi = createApi({
	reducerPath: 'notificationsApi',
	tagTypes: ['Notification'],
	baseQuery: fetchBaseQuery({
		baseUrl: import.meta.env.VITE_NOTIFICATIONS_URL,
		credentials: 'include',
	}),
	endpoints: (build) => ({
		getNotifications: build.query<NotificationsListResponse, void>({
			query: () => '/notifications',
			providesTags: ['Notification'],
		}),
		markAsRead: build.mutation<void, number>({
			query: (id) => ({
				url: `/notifications/${id}/read`,
				method: 'PATCH',
			}),
			invalidatesTags: ['Notification'],
		}),
	}),
});

export const { useGetNotificationsQuery, useMarkAsReadMutation } = notificationsApi;
