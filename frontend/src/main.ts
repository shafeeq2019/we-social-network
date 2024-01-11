import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'


axios.defaults.baseURL = "http://127.0.0.1:8000"


const app = createApp(App)

// Add Axios to the Vue prototype
app.config.globalProperties.$axios = axios;

app.use(createPinia())
app.use(router)
app.mount('#app')
