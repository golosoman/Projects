import { ref, onMounted } from 'vue'
// import {API_PORT, API_HOST} from '@/config.js'
import axios from '@/axiosConfig'
// import postsList from '@/data/posts.json'

export const usePosts = () => {
  const posts = ref([])

  onMounted(async () => {
    // posts.value = postsList
    try {
      const response = await axios.get(`/posts`)
      posts.value = response.data;
      console.log(posts.value, "Мои посты");
    } catch (error) {
      console.log("Произошла ошибка: ", error)
    }
  
    // console.log(postsList, "postsList")
  })
  return posts
}
