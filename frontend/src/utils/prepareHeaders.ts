// src/utils/prepareHeaders.ts
import { RootState } from '@/store/store'; // Импортируйте тип состояния из вашего стора
import { FetchBaseQueryMeta } from '@reduxjs/toolkit/query';

export const prepareHeaders = (headers: Headers, _state: RootState) => {
  return headers;
};
