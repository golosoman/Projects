import { createApp } from 'vue'
import router from '@/router/router'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'


const app = createApp(App)

// app.config.globalProperties.$axios = axios;
app.use(router);
app.use(bootstrap);
app.mount("#app");