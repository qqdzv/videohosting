import { api } from './api';
import { GetVideo, EditVideo, BaseResponse } from '../../api/types';

interface GetVideosParams {
  offset?: number;
  limit?: number;
  is_random?: boolean;
}

interface UploadVideoParams {
  file: File;
  title: string;
  description: string;
}

const DEFAULT_PARAMS: GetVideosParams = {
  offset: 0,
  limit: 100,
  is_random: true
};

export const videoApi = api.injectEndpoints({
  endpoints: (build) => ({
    uploadVideo: build.mutation<Record<string, string>, UploadVideoParams>({
      query: ({ file, title, description }) => {
        const formData = new FormData();
        formData.append('file', file);
        return {
          url: `/videos?title=${title}&description=${description}`,
          method: 'POST',
          body: formData,
        };
      },
      invalidatesTags: ['Video'],
    }),

    getVideo: build.query<GetVideo, number>({
      query: (videoId) => `/videos/${videoId}`,
      providesTags: ['Video'],
    }),

    editVideo: build.mutation<BaseResponse, { videoId: number; data: EditVideo }>({
      query: ({ videoId, data }) => ({
        url: `/videos/${videoId}`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: ['Video'],
    }),

    deleteVideo: build.mutation<BaseResponse, number>({
      query: (videoId) => ({
        url: `/videos/${videoId}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Video'],
    }),

    addVideoView: build.mutation<BaseResponse, number>({
      query: (videoId) => ({
        url: `/videos/${videoId}/views`,
        method: 'POST',
      }),
      invalidatesTags: ['Video'],
    }),

    getVideos: build.query<GetVideo[], GetVideosParams | undefined>({
      query: (params) => ({
        url: '/videos',
        params: params || DEFAULT_PARAMS,
      }),
      providesTags: ['Video'],
    }),

    searchVideos: build.query<GetVideo[], string>({
      query: (query) => ({
        url: '/videos/search',
        params: { query: query },
      }),
      providesTags: ['Video'],
    }),

    getVideosByAuthor: build.query<GetVideo[], string>({
      query: (authorUsername) => `/videos/author/${authorUsername}`,
      providesTags: ['Video'],
    }),

    processOldVideo: build.mutation<BaseResponse, number>({
      query: (videoId) => ({
        url: `/videos/process/${videoId}`,
        method: 'POST',
      }),
      invalidatesTags: ['Video'],
    }),

    getHistory: build.query<GetVideo[], void>({
      query: () => '/videos/history',
      providesTags: ['Video'],
    }),
  }),
});

export const {
  useUploadVideoMutation,
  useGetVideoQuery,
  useEditVideoMutation,
  useDeleteVideoMutation,
  useAddVideoViewMutation,
  useGetVideosQuery,
  useSearchVideosQuery,
  useGetVideosByAuthorQuery,
  useProcessOldVideoMutation,
  useGetHistoryQuery,
} = videoApi; 