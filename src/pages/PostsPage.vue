<script>
import PostList from '@/components/PostList.vue'
import { usePosts } from '@/hooks/usePosts.js'

export default {
  components: {
    PostList
  },
  setup() {
    const posts = usePosts()
    return posts
  }
}
</script>
<template>
  <div class="content">
    <PostList :post-list="posts" />
  </div>
</template>

<style scoped></style>
