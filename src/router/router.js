import { createWebHistory, createRouter } from 'vue-router'

import MainPage from '@/pages/MainPage.vue'
import PostIdPage from '@/pages/PostIdPage.vue'
import PostsPage from '@/pages/PostsPage.vue'
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
]

const router = createRouter({
  routes,
  history: createWebHistory()
})

export default router;
