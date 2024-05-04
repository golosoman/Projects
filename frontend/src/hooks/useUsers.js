import { ref, onMounted } from 'vue'
import usersList from '@/data/users.json'

export const useUsers = () => {
  const users = ref([])

  onMounted(() => {
    users.value = usersList
  })
  return users
}
