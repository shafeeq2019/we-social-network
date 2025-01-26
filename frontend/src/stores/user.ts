import { defineStore } from 'pinia';
import axios from 'axios';
import { State, Token, LoginUser } from '../interfaces.ts';

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
      console.log('initStore', localStorage.getItem('user.access'));

      if (localStorage.getItem('user.access')) {
        console.log('User has access!');
        this.user.access = localStorage.getItem('user.access') || '';
        this.user.refresh = localStorage.getItem('user.refresh') || '';
        this.user.id = localStorage.getItem('user.id') || '';
        this.user.name = localStorage.getItem('user.name') || '';
        this.user.email = localStorage.getItem('user.email') || '';
        this.user.avatar_link = localStorage.getItem('user.avatar_link') || '';
        this.user.isAuthenticated = true;
        console.log(this.user.id);
        this.refreshToken();

        console.log('Initialized user:', this.user);
      }
    },

    setToken(data: Token) {
      console.log('setToken', data);

      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;

      localStorage.setItem('user.access', data.access);
      localStorage.setItem('user.refresh', data.refresh);

      console.log('user.access: ', localStorage.getItem('user.access'));
    },

    removeToken() {
      console.log('removeToken');

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
      console.log('setUserInfo', user);

      this.user.id = user.id;
      this.user.name = user.name;
      this.user.email = user.email;
      this.user.avatar_link = user.avatar_link;

      localStorage.setItem('user.id', this.user.id);
      localStorage.setItem('user.name', this.user.name);
      localStorage.setItem('user.email', this.user.email);
      localStorage.setItem('user.avatar_link', this.user.avatar_link);

      console.log('User', this.user);
    },

    refreshToken() {
      axios.post('/api/refresh/', {
        refresh: this.user.refresh
      })
        .then((response) => {
          this.user.access = response.data.access;

          localStorage.setItem('user.access', response.data.access);

          axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access;
        })
        .catch((error) => {
          console.log(error);

          this.removeToken();
        });
    },
  }
});
