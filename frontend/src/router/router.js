import { createWebHistory, createRouter } from 'vue-router'

import MainPage from '@/pages/MainPage.vue'
import PostIdPage from '@/pages/PostIdPage.vue'
import PostsPage from '@/pages/PostsPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'
import AuthPage from '@/pages/AuthPage.vue'
import Secure from '@/components/Secure.vue'
import store from '@/store/index.js'
// import PostIdPage from '@/pages/PostIdPage.vue'
// import PostsPage from '@/pages/PostsPage.vue'

const routes = [
  {
    path: '/posts/:id',
    name: "post",
    component: PostIdPage,
    props: true
  },
  {
    path: '/',
    name: 'posts',
    component: PostsPage
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  {
    path: '/login',
    name: 'login',
    component: AuthPage
  },
  // {
  //   path: '/rersonal-account',
  //   name: 'p-account',
  //   component: <template><div>Нифига себе</div></template>
  // },
  {
    path: '/secure',
    name: 'secure',
    component: Secure,
    meta: { 
      requiresAuth: true
    }
  },
]

const router = createRouter({
  routes,
  history: createWebHistory()
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login') 
  } else {
    next() 
  }
})

export default router;
