import { ref, onMounted } from 'vue'
import axios from '@/axiosConfig'

export const useUser = () => {
    const user = ref([])
    const isUserLoading = ref(true)

    onMounted(async () => {
        try {
            const response = await axios.get(`/auth/login/user`)
            user.value = response.data
            console.log(user.value, 'Мой пользователь')
        } catch (error) {
            console.log('Произошла ошибка: ', error)
        } finally {
            isUserLoading.value = false
        }
    })
    return { user, isUserLoading }
}

