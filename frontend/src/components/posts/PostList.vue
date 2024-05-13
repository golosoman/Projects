<script setup>
import { defineProps } from 'vue'
import PostCard from '@/components/posts/PostCard.vue'

const props = defineProps({
    postList: {
        type: Array,
        require: true
    }
})
const emits = defineEmits(['delPost'])

const deletePost = (id) => {
    emits('delPost', id)
}

console.log(props.postList, 'PostList')
</script>

<template>
    <div class="posts_content p-3" v-for="(post, index) in props.postList" :key="index">
        <PostCard :post="post" @del-post="deletePost"/>
    </div>
</template>

<style scoped></style>
