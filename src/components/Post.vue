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
  <div v-if="props.post.status" class="post">
    <div class="title">
      <span>{{ props.post.title }}</span>
    </div>
    <div class="description">
      <span>{{ props.post.description }}</span>
    </div>
    <div class="date_publication">
      <span>{{ props.post.dateTime }}</span>
    </div>
  </div>
</template>

<style scoped></style>
