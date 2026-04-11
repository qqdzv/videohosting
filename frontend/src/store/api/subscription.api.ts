import { api } from './api';
import { BaseResponse, SubscriptionAuthorView, AuthorView } from '../../api/types';

export const subscriptionApi = api.injectEndpoints({
	endpoints: (build) => ({
		subscribe: build.mutation<BaseResponse, string>({
			query: (followUsername) => ({
				url: `/subscriptions//${followUsername}`,
				method: 'POST'
			}),
			invalidatesTags: ['Subscription']
		}),

		unsubscribe: build.mutation<BaseResponse, string>({
			query: (followUsername) => ({
				url: `/subscriptions/${followUsername}`,
				method: 'DELETE'
			}),
			invalidatesTags: ['Subscription']
		}),

		getMySubscriptions: build.query<SubscriptionAuthorView[], void>({
			query: () => '/subscriptions',
			providesTags: ['Subscription']
		}),

		isSubscribed: build.query<{ success: boolean }, string>({
			query: (username) => ({
				url: `/subscriptions/${username}`,
				method: 'GET'
			}),
			providesTags: ['Subscription']
		}),

		searchChannels: build.query<AuthorView[], string>({
			query: (query) => ({
				url: `/subscriptions/search`,
				method: 'GET',
				params: {
					query: query
				}
			}),
			providesTags: ['Subscription']
		})
	})
});

export const {
	useSubscribeMutation,
	useUnsubscribeMutation,
	useGetMySubscriptionsQuery,
	useIsSubscribedQuery,
	useSearchChannelsQuery
} = subscriptionApi;
