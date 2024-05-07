<!-- eslint-disable vue/multi-word-component-names -->
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
  <div class="card mb-4">
    <div class="card-header bg-white">
      <div class="content p-2">
          <h3>{{ props.post.title }}</h3>
          <div class="d-flex flex-row align-items-center mt-3">
              <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(4).webp" alt="avatar" width="25"
              height="25" />
              <p class="small mb-0 ms-2"><span>Пользователь: </span></p>
          </div>
          <div class="d-flex flex-row align-items-left mt-3">
              <p class="small text-muted mb-0">Дата: {{ props.post.published_at }}</p>
          </div>
        </div>
    </div>
    <div class="card-body">
        <p>{{ props.post.content }}</p>
    </div>
  </div>
</template>

<style scoped>
</style>
