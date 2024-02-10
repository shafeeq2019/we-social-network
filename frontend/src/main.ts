import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import "./firebase.ts";
import App from './App.vue'
import router from './router'
import axios from 'axios'

const VITE_API_URL = import.meta.env.VITE_API_URL;

axios.interceptors.request.use(config => {
    config.baseURL = VITE_API_URL;
    return config;
  }, error => {
    return Promise.reject(error);
  });
  

const app = createApp(App)

// Add Axios to the Vue prototype
app.config.globalProperties.$axios = axios;

app.use(createPinia())
app.use(router)
app.mount('#app')
