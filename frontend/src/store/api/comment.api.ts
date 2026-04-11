import { api } from './api';
import { CommentView, CommentCreate, CommentEdit, BaseResponse } from '../../api/types';

export const commentApi = api.injectEndpoints({
  endpoints: (build) => ({
    getComments: build.query<CommentView[], number>({
      query: (videoId) => `/videos/${videoId}/comments`,
      providesTags: ['Comment'],
    }),

    createComment: build.mutation<BaseResponse, { videoId: number; data: CommentCreate }>({
      query: ({ videoId, data }) => ({
        url: `/videos/${videoId}/comments`,
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Comment'],
    }),

    editComment: build.mutation<BaseResponse, { commentId: number; data: CommentEdit }>({
      query: ({ commentId, data }) => ({
        url: `/comments/${commentId}`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: ['Comment'],
    }),

    deleteComment: build.mutation<void, number>({
      query: (commentId) => ({
        url: `/comments/${commentId}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Comment'],
    }),
  }),
});

export const {
  useGetCommentsQuery,
  useCreateCommentMutation,
  useEditCommentMutation,
  useDeleteCommentMutation,
} = commentApi; 