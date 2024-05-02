<script setup>
import { defineProps } from 'vue'
import Post from '@/components/Post.vue'

const props = defineProps({
  postList: {
    type: Array,
    require: true
  }
})
</script>

<template>
  <div class="posts_content" v-for="(post, index) in props.postList" :key="index">
    <Post :post="post" />
  </div>
</template>

<style scoped></style>
