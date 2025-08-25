import { AxiosError, AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { useAuthStore } from '@/common/store/auth.store';

export function refreshTokenInterceptor(api: AxiosInstance) {
  return async function (
    error: AxiosError,
  ): Promise<AxiosResponse<unknown>> {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    };

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshResponse = await api.post<{ access_token: string }>("/auth/refresh");
        const newAccessToken = refreshResponse.data.access_token;

        useAuthStore.getState().login(newAccessToken);

        (originalRequest.headers as unknown as import("axios").AxiosHeaders).set(
          "Authorization",
          `Bearer ${newAccessToken}`,
        );

        return api(originalRequest);
      } catch (refreshError) {
        useAuthStore.getState().logout();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  };
}