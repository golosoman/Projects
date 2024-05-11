import { ref, onMounted } from 'vue'
import axios from '@/axiosConfig'

export const usePostById = (id) => {
    const post = ref([])
    const isPostLoading = ref(true)

    onMounted(async () => {
        try {
            const response = await axios.get(`/posts/${id}`)
            post.value = response.data
            console.log(post.value, 'Мои посты по идентификатору')
        } catch (error) {
            console.log('Произошла ошибка: ', error)
        } finally {
            isPostLoading.value = false
        }
    })
    return { post, isPostLoading }
}
