<script setup>
import { defineProps } from 'vue'
import Comment from '@/components/comments/Comment.vue'

const props = defineProps({
    commentsList: {
        type: Array,
        require: true
    }
})
</script>

<template>
    <div v-if="props.commentsList.length === 0">
        <p>Комментарии отсутствуют будьте первым!</p>
    </div>
    <TransitionGroup name="comments-list">
        <Comment :comment="comment" v-for="comment in props.commentsList" :key="comment.id" />
    </TransitionGroup>
</template>

<style scoped>
.comments-list-item {
    display: inline-block;
    margin-right: 10px;
}
.comments-list-enter-active,
.comments-list-leave-active {
    transition: all 0.4s ease;
}
.comments-list-enter-from,
.comments-list-leave-to {
    opacity: 0;
    transform: translateX(130px);
}
.comments-list-move {
    transition: transform 0.4s ease;
}
</style>
