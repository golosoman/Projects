<script setup>
import { defineProps } from 'vue'
import PostCard from '@/components/PostCard.vue'

const props = defineProps({
  postList: {
    type: Array,
    require: true
  }
})
console.log(props.postList, "PostList")
</script>

<template>
    <div class="posts_content p-3" v-for="(post, index) in props.postList" :key="index">
      <PostCard :post="post" />
    </div>
</template>

<style scoped></style>
