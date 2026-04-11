import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { IUser } from '@/types/auth.types'

interface AuthState {
	user: IUser | null
	isAuthenticated: boolean
}

const initialState: AuthState = {
	user: null,
	isAuthenticated: false,
}

export const authSlice = createSlice({
	name: 'auth',
	initialState,
	reducers: {
		setCredentials: (state) => {
			state.isAuthenticated = true
		},
		setUser: (state, action: PayloadAction<IUser>) => {
			state.user = action.payload
			state.isAuthenticated = true
		},
		logout: (state) => {
			state.user = null
			state.isAuthenticated = false
		}
	}
})

export const { actions, reducer } = authSlice
