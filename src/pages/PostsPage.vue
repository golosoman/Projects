<script>
import PostList from '@/components/PostList.vue'
import { usePosts } from '@/hooks/usePosts.js'

export default {
  components: {
    PostList
  },
  setup() {
    const posts = usePosts()
    console.log(posts, "PostPage");
    return {posts}
  }
}
</script>

<template>
  <div class="post-list-content">
    <post-list
      :postList="posts"
    />
    <!-- <PostList :post-list="posts" /> -->
  </div>
</template>

<style scoped></style>
