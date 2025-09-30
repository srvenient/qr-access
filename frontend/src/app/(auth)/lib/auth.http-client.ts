import {BaseHttpClient} from "@/common/http-client/http-client";
import config from "@/config/config";
import axios from "axios";
import {ApiError} from "@/common/errors/api-error";

export class AuthHttpClient extends BaseHttpClient {
  constructor() {
    super({
      baseURL: config.clients.fastapi.baseURL,
      timeout: config.clients.fastapi.timeout,
      keepAlive: config.clients.fastapi.keepAlive,
    });
  }

  async login(username: string, password: string): Promise<void> {
    try {
      await this.instance.post(
        '/auth/login',
        new URLSearchParams({username, password}),
        {
          headers: {"Content-Type": "application/x-www-form-urlencoded"}
        }
      );
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
}

export const authHttpClient = new AuthHttpClient();