import { ref, onMounted } from 'vue'
import postsList from '@/data/posts.json'

export const usePosts = () => {
  const posts = ref([])

  onMounted(() => {
    posts.value = postsList
    // console.log(postsList, "postsList")
  })
  console.log(posts, "usePosts")
  return posts
}
