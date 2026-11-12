import { defineStore } from 'pinia';
import axios from 'axios';
import { State, Token, LoginUser } from '../interfaces.ts';

// Shared promise so parallel 401s trigger only one refresh request
let refreshPromise: Promise<string> | null = null;

export const useUserStore = defineStore('user', {
  state: (): State => ({
    user: {
      isAuthenticated: false,
      id: '',
      name: '',
      email: '',
      access: '',
      refresh: '',
      avatar_link: ''
    }
  }),

  actions: {
    initStore() {
      if (localStorage.getItem('user.access')) {
        this.user.access = localStorage.getItem('user.access') || '';
        this.user.refresh = localStorage.getItem('user.refresh') || '';
        this.user.id = localStorage.getItem('user.id') || '';
        this.user.name = localStorage.getItem('user.name') || '';
        this.user.email = localStorage.getItem('user.email') || '';
        this.user.avatar_link = localStorage.getItem('user.avatar_link') || '';
        this.user.isAuthenticated = true;
        this.refreshToken().catch(() => {
          // removeToken() already ran; the 401 interceptor handles redirects
        });
      }
    },

    setToken(data: Token) {
      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;

      localStorage.setItem('user.access', data.access);
      localStorage.setItem('user.refresh', data.refresh);
    },

    removeToken() {
      this.user.refresh = '';
      this.user.access = '';
      this.user.isAuthenticated = false;
      this.user.id = '';
      this.user.name = '';
      this.user.email = '';
      this.user.avatar_link = '';

      localStorage.setItem('user.access', '');
      localStorage.setItem('user.refresh', '');
      localStorage.setItem('user.id', '');
      localStorage.setItem('user.name', '');
      localStorage.setItem('user.email', '');
      localStorage.setItem('user.avatar_link', '');
    },

    setUserInfo(user: LoginUser) {
      this.user.id = user.id;
      this.user.name = user.name;
      this.user.email = user.email;
      this.user.avatar_link = user.avatar_link;

      localStorage.setItem('user.id', this.user.id);
      localStorage.setItem('user.name', this.user.name);
      localStorage.setItem('user.email', this.user.email);
      localStorage.setItem('user.avatar_link', this.user.avatar_link);
    },

    /**
     * Gets a new access token with the refresh token and resolves with it.
     * Logs the user out when the refresh token is invalid or expired.
     */
    refreshToken(): Promise<string> {
      if (!refreshPromise) {
        refreshPromise = axios.post('/api/refresh/', {
          refresh: this.user.refresh
        })
          .then((response) => {
            this.user.access = response.data.access;
            localStorage.setItem('user.access', response.data.access);

            // ROTATE_REFRESH_TOKENS: the backend also returns a new refresh token
            if (response.data.refresh) {
              this.user.refresh = response.data.refresh;
              localStorage.setItem('user.refresh', response.data.refresh);
            }
            return response.data.access as string;
          })
          .catch((error) => {
            this.removeToken();
            throw error;
          })
          .finally(() => {
            refreshPromise = null;
          });
      }
      return refreshPromise;
    },
  }
});
