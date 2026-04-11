export interface IAuthResponse {
  access_token: string;
  refresh_token: string;
  user: IUser;
}

export interface IUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  avatar?: string;
  total_subscribers: number;
}

export interface ILoginRequest {
  email: string;
  password: string;
}

export interface IRegisterRequest {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export type ValidationErrors = Partial<Record<keyof IRegisterRequest, string>>; 