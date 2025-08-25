import {BaseHttpClient} from "@/common/http-client/http-client";
import config from "@/config/config";
import {ApiError} from "@/common/errors/api-error";
import axios from "axios";
import {useAuthStore} from "@/common/store/auth.store";

export class AuthHttpClient extends BaseHttpClient {
  constructor() {
    super({
      baseURL: config.clients.fastapi.baseURL,
      timeout: config.clients.fastapi.timeout,
      keepAlive: config.clients.fastapi.keepAlive,
      withCredentials: config.clients.fastapi.withCredentials,
    });
  }

  async login(username: string, password: string): Promise<boolean> {
    try {
      const response = await this.instance.post(
        'auth/login',
        new URLSearchParams({username, password}),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      );

      const {access_token} = response.data;

      useAuthStore.getState()
        .login(access_token);

      return true;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new ApiError(
          error.response.data?.message ?? 'Credentials are not valid',
          error.response.status
        );
      }

      throw new ApiError('Server error', 500);
    }
  }

  async logout(): Promise<void> {
    useAuthStore.getState().logout();
  }
}

export const authHttpClient = new AuthHttpClient();