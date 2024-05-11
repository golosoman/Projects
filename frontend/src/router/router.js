import { createWebHistory, createRouter } from 'vue-router'
// import MainPage from '@/pages/MainPage.vue'
import PostIdPage from '@/pages/posts/PostIdPage.vue'
import PostsPage from '@/pages/posts/PostsPage.vue'
import RegisterPage from '@/pages/auth/RegisterPage.vue'
import AuthPage from '@/pages/auth/AuthPage.vue'
import AddPostPage from '@/pages/posts/AddPostPage.vue'
import store from '@/store/index.js'
import CabinetPage from '@/pages/CabinetPage.vue'
// import PostIdPage from '@/pages/PostIdPage.vue'
// import PostsPage from '@/pages/PostsPage.vue'

const routes = [
    {
        path: '/posts/:id',
        name: 'post',
        component: PostIdPage,
        props: true
    },
    {
        // main
        path: '/posts',
        name: 'posts',
        component: PostsPage
    },
    {
        path: '/posts/add',
        name: 'post-add',
        component: AddPostPage,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/auth/register',
        name: 'register',
        component: RegisterPage,
        meta: {
            requiresAuth: false
        }
    },
    {
        path: '/auth/login',
        name: 'login',
        component: AuthPage,
        meta: {
            requiresAuth: false
        }
    },
    {
        path: '/auth/login/cabinet',
        name: 'cabinet',
        component: CabinetPage,
        meta: {
            requiresAuth: true
        }
    },
    // {
    //   path: '/rersonal-account',
    //   name: 'p-account',
    //   component: <template><div>Нифига себе</div></template>
    // },
    {
        path: '/',
        redirect: '/posts'
    }
]

const router = createRouter({
    routes,
    history: createWebHistory()
})

router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (store.getters.isLoggedIn) {
            next()
            return
        }
        next('/auth/login')
    } else {
        next()
    }
})

export default router
