// Auth Types
export interface AvatarPresignedUrlResponse {
  presigned_url: string;
  key: string;
}


export interface UserLoginForm {
  email: string;
  password: string;
}

export interface UserRegistrationForm {
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  password: string;
}

export interface UserEditForm {
  first_name?: string;
  last_name?: string;
  username?: string;
  email?: string;
}

export interface JwtResponse {
  access_token: string;
  user: UserProfile;
}

export interface UserProfile {
  id: number;
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  avatar?: string;
  total_subscribers: number;  
}

// Video Types
export interface GetVideo {
  id: number;
  title: string;
  description?: string;
  video_url?: string;
  preview_url?: string;
  quality?: string;
  duration?: number;
  video_hls?: string;
  views: number;
  author: AuthorView;
  reaction?: Like;
  process_status?: boolean;
  likes?: number;
  dislikes?: number;
  created_at: string;
}

export interface EditVideo {
  title?: string;
  description?: string;
}

export interface AuthorView {
  username: string;
  first_name: string;
  last_name: string;
  total_subscribers: number;
  avatar?: string;
}

// Comment Types
export interface CommentCreate {
  text?: string;
}

export interface CommentEdit {
  text?: string;
}

export interface CommentView {
  id?: number;
  text?: string;
  username?: string;
  first_name?: string;
  last_name?: string;
  avatar?: string;
  created_at?: string;
}

// Like Types
export type Like = 'like' | 'dislike';

export interface IsLikedRequest {
  reaction: Like;
}

// Subscription Types
export interface SubscriptionAuthorView extends AuthorView {
  id?: number;
}

// Base Response
export interface BaseResponse {} 