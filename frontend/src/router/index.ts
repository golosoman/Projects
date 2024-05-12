import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/pages/MainPage.vue'
import AboutMe from '@/pages/AboutMe.vue'
import BMICalculatorPage from '@/pages/calculators/BMICalculatorPage.vue'
import RIDDCalculatorPage from '@/pages/calculators/RIDDCalculatorPage.vue'
import TitrationCalculatorPage from '@/pages/calculators/TitrationCalculatorPage.vue'

const routes = [
    {
        path: '/',
        name: 'main',
        component: MainPage
    },
    {
        path: '/about',
        name: 'about',
        component: AboutMe
    },
    {
        path: '/calculator/body-mass-index',
        name: 'BMI',
        component: BMICalculatorPage
    },
    {
        path: '/calculator/titration-rate',
        name: 'TR',
        component: TitrationCalculatorPage
    },
    {
        path: '/calculator/rate-intravenous-drip-drug',
        name: 'RIDD',
        component: RIDDCalculatorPage
    }
]

const router = createRouter({
    routes,
    history: createWebHistory()
})

export default router
