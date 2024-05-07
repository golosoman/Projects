<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  comment: {
    type: Object,
    require: true
  }
})
</script>

<template>
    <div class="content">
        <div class="card mb-4">
        <div class="card-body">
            <p>{{ props.comment.message }}</p>

            <div class="d-flex justify-content-between">
            <div class="d-flex flex-row align-items-center">
                <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(4).webp" alt="avatar" width="25"
                height="25" />
                <p class="small mb-0 ms-2"><span>Пользователь: {{ props.comment.author.name }} ({{ props.comment.author.reputation }})</span></p>
            </div>
            <div class="d-flex flex-row align-items-center">
                <p class="small text-muted mb-0">Дата: {{ props.comment.published_at }}</p>
            </div>
            </div>
        </div>
        </div>
    </div>
</template>

<style scoped>
  
</style>
