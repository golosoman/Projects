<template>
  <div class="content">
    <post :post="post"></post>
  </div>
</template>

<script>
import Post from '@/components/Post.vue'
import { usePostById } from '@/hooks/post/usePostById';
export default {
  components: {
    Post
  },
  setup() {
    const post = usePostById()
    return { post }
  }
}
</script>

<style scoped></style>
