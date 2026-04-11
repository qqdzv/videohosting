import { configureStore } from '@reduxjs/toolkit'

import { api } from '@/api/api.ts'
import { notificationsApi } from '@/api/notifications.api.ts'
import { reducer as authReducer } from '@/store/auth/auth.slice.ts'

export const store = configureStore({
	reducer: {
		[api.reducerPath]: api.reducer,
		[notificationsApi.reducerPath]: notificationsApi.reducer,
		auth: authReducer
	},
	middleware: (getDefaultMiddleware) =>
		getDefaultMiddleware()
			.concat(api.middleware)
			.concat(notificationsApi.middleware),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
