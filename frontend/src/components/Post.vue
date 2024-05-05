<script setup>
import { defineProps } from 'vue'
const props = defineProps({
  post: {
    type: Object,
    require: true
  }
})
</script>

<template>
  <div v-if="props.post.status">
    <div class="card text-center">
      <div class="card-header">
        <h3>{{ props.post.title }}</h3>
      </div>
      <div class="card-body">
        <p class="card-text">{{ props.post.content }}</p>
        <a @click="$router.push(`/posts/${props.post.id}`)" class="btn btn-dark">Перейти</a>
      </div>
      <div class="card-footer text-muted">
        {{ props.post.published_at }}
      </div>
    </div>
  </div>
</template>

<style scoped>
  
</style>
