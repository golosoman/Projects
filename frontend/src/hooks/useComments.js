import { ref, onMounted } from 'vue'
import commentsList from '@/data/comments.json'

export const useComments = () => {
  const comments = ref([])

  onMounted(() => {
    comments.value = commentsList
  })
  return comments
}
