import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { useUserStore } from './stores/user';

const VITE_API_URL = import.meta.env.VITE_API_URL;

// These endpoints don't use the access token, so a 401 there must not trigger a refresh
const AUTH_ENDPOINTS = ['/api/login/', '/api/refresh/', '/api/signup/'];

const app = createApp(App);

// Add Axios to the Vue prototype
app.config.globalProperties.$axios = axios;

app.use(createPinia());

const userStore = useUserStore();

axios.interceptors.request.use(config => {
  config.baseURL = VITE_API_URL;
  // Always send the current token from the store (it changes after a refresh)
  if (userStore.user.access && !AUTH_ENDPOINTS.includes(config.url ?? '')) {
    config.headers.Authorization = `Bearer ${userStore.user.access}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Expired access token: refresh it once and repeat the request
axios.interceptors.response.use(response => response, async (error: AxiosError) => {
  const request = error.config as (InternalAxiosRequestConfig & { _retried?: boolean }) | undefined;

  if (error.response?.status !== 401 || !request || request._retried || AUTH_ENDPOINTS.includes(request.url ?? '')) {
    return Promise.reject(error);
  }

  if (!userStore.user.refresh) {
    userStore.removeToken();
    router.push({ name: 'login', query: { redirect: router.currentRoute.value.fullPath } });
    return Promise.reject(error);
  }

  request._retried = true;
  try {
    await userStore.refreshToken();
  } catch {
    router.push({ name: 'login', query: { redirect: router.currentRoute.value.fullPath } });
    return Promise.reject(error);
  }
  // The request interceptor adds the new token
  return axios(request);
});

app.use(router);
app.mount('#app');
