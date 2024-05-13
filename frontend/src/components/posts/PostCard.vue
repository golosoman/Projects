<!-- eslint-disable vue/multi-word-component-names -->
<script setup>
import { defineProps, defineEmits } from 'vue'
import axios from '@/axiosConfig';
const props = defineProps({
    post: {
        type: Object,
        require: true
    },
})

const emits = defineEmits(['delPost'])

const confirmPost = () => {
    try {
        axios.patch(`posts/${props.post.id}/confirm`)
        emits('delPost', props.post.id)

    } catch (error) {
        console.log(error.message)
    }
}

</script>

<template>
    <div>
        <div class="card text-center">
            <div class="card-header">
                <h3>{{ props.post.title }}</h3>
            </div>
            <div class="card-body">
                <p class="card-text">{{ props.post.content }}</p>
                <a v-if="post.status" @click="$router.push(`/posts/${props.post.id}`)" class="btn btn-dark">Перейти</a>
                <a v-else @click="confirmPost" class="btn btn-success">Разрешить</a>
            </div>
            <div class="card-footer text-muted">
                {{ props.post.published_at }}
            </div>
        </div>
    </div>
</template>

<style scoped></style>
