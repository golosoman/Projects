import { createWebHistory, createRouter } from 'vue-router'

import MainPage from '@/pages/MainPage.vue'
import PostIdPage from '@/pages/PostIdPage.vue'
import PostsPage from '@/pages/PostsPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'
import AuthPage from '@/pages/AuthPage.vue'
// import PostIdPage from '@/pages/PostIdPage.vue'
// import PostsPage from '@/pages/PostsPage.vue'

const routes = [
  {
    path: '/',
    component: MainPage
  },
  {
    path: '/posts/:id',
    component: PostIdPage
  },
  {
    path: '/posts',
    component: PostsPage
  },
  {
    path: '/register',
    component: RegisterPage
  },
  {
    path: '/authorization',
    component: AuthPage
  },
]

const router = createRouter({
  routes,
  history: createWebHistory()
})

export default router;
