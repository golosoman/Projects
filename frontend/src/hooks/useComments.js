import { ref, onMounted } from 'vue'
import axios from '@/axiosConfig'

export const useComments = (id) => {
  const comments = ref([])

  onMounted(async () => {
    // posts.value = postsList
    try {
      const response = await axios.get(`/posts/${id}/comments`)
      
      comments.value = response.data;
      console.log(comments.value, "Мои комментарии");
    } catch (error) {
      console.log("Произошла ошибка: ", error)
    }
  
    // console.log(postsList, "postsList")
  })
  return comments
}
