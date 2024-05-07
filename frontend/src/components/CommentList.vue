<script setup>
import { defineProps } from 'vue'
import Comment from '@/components/Comment.vue'

const props = defineProps({
  commentsList: {
    type: Array,
    require: true
  }
})
console.log(props.postList, "CommentsList")
</script>

<template>
    <div v-if="props.commentsList.length === 0">
        <p>Комментарии отсутствуют</p>
    </div>
    <div v-else v-for="(comment, index) in props.commentsList" :key="index" class="comments_content p">
        <Comment :comment="comment" />
    </div>
</template>

<style scoped></style>
