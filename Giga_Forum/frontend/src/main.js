import { createApp } from 'vue'
import router from '@/router/router'
import App from './App.vue'
import "bootstrap/dist/css/bootstrap.min.css"
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'
// import { BAlert } from 'bootstrap-vue'
import store from '@/store/index.js'
import Axios from 'axios'
import components from '@/components/UI'

const app = createApp(App)

app.config.globalProperties.$http = Axios

const token = localStorage.getItem('token')
if (token) {
    app.config.globalProperties.$http.defaults.headers.common['Authorization'] = token
}

// app.component('b-alert', BAlert)

components.forEach((component) => {
    app.component(component.name, component)
})

app.use(store).use(router).use(bootstrap).mount('#app')
