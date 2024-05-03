import { ref, onMounted } from 'vue'
import postsList from '@/data/comments.json'

export const useComments = () => {
  const comments = ref([])

  onMounted(() => {
    comments.value = postsList
  })
  return comments
}
