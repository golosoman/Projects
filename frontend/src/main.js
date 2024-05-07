import { createApp } from 'vue'
import router from '@/router/router'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'
import store from '@/store/index.js';
import Axios from 'axios'
// import Vue from "vue"

// Vue.prototype.$http = Axios;

// const token = localStorage.getItem('token')
// if (token) {
//   Vue.prototype.$http.defaults.headers.common['Authorization'] = token
// }

const app = createApp(App)

app.config.globalProperties.$http=Axios;
const token = localStorage.getItem('token')
if (token) {
  app.config.globalProperties.$http.defaults.headers.common['Authorization'] = token
}
// app.config.globalProperties.$axios = axios;
app.use(store)
app.use(router);
app.use(bootstrap);
app.mount("#app");