import { ref, onMounted } from 'vue'
// import {API_PORT, API_HOST} from '@/config.js'
import axios from 'axios';
// import postsList from '@/data/posts.json'

export const usePostById = (id) => {
  const posts = ref([])

  onMounted(async () => {
    // posts.value = postsList
    try {
      const response = await axios.get(`/posts/${id}`)
      posts.value = response.data;
      console.log(posts.value, "Мои данные");
    } catch (error) {
      console.log("Произошла ошибка: ", error)
    }
  
    // console.log(postsList, "postsList")
  })
  console.log(posts, "usePosts")
  return posts
}