import { api } from './api';
import { IsLikedRequest } from '../../api/types';

export const likeApi = api.injectEndpoints({
  endpoints: (build) => ({
    setLike: build.mutation<boolean, { videoId: number; data: IsLikedRequest }>({
      query: ({ videoId, data }) => ({
        url: `/videos/${videoId}/likes`,
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Video'],
    }),
  }),
});

export const { useSetLikeMutation } = likeApi; 