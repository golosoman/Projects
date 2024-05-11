import { ref, onMounted } from 'vue'
import axios from '@/axiosConfig'

export const usePosts = () => {
    const posts = ref([])
    const isPostsLoading = ref(true)

    onMounted(async () => {
        try {
            const response = await axios.get(`/posts`)
            posts.value = response.data
            console.log(posts.value, 'Мои посты')
        } catch (error) {
            console.log('Произошла ошибка: ', error)
        } finally {
            isPostsLoading.value = false
        }
    })
    return { posts, isPostsLoading }
}
