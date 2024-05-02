import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/pages/MainPage.vue'
// import PostIdPage from '@/pages/PostIdPage.vue'
// import PostsPage from '@/pages/PostsPage.vue'

const routes = [
  {
    path: '/',
    component: MainPage
  }
]

const router = createRouter({
  routes,
  history: createWebHistory()
})

export default router
