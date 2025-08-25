import { create } from 'zustand';
import { persist } from 'zustand/middleware';

type AuthState = {
  isAuthenticated: boolean;
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isAuthenticated: false,
      token: null,
      user: null,
      login: (token: string) =>
        set(() => ({
          isAuthenticated: true,
          token,
        })),
      logout: () =>
        set(() => ({
          isAuthenticated: false,
          token: null,
        })),
    }),
    {
      name: 'auth-storage',
    },
  ),
);