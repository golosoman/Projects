<script>
import PostList from '@/components/PostList.vue'
import { usePosts } from '@/hooks/post/usePosts.js'

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
  <div class="content row d-flex justify-content-center">
    <div class="content w-75">
      <post-list
        :postList="posts"
      />
      <!-- <PostList :post-list="posts" /> -->
    </div>
  </div>
</template>

<style scoped></style>
