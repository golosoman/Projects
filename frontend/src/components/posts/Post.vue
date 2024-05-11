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
                <div class="d-flex flex-row align-items-center">
                    <img
                        src="https://i.livelib.ru/auface/1062661/o/ec53/Dmitrij_Lyubchenko.jpg"
                        alt="avatar"
                        width="25"
                        height="25"
                    />
                    <p class="small mb-0 ms-2">
                        <span
                            >Пользователь: {{ props.post.author.name }} ({{
                                props.post.author.reputation
                            }})</span
                        >
                    </p>
                </div>
                <div class="d-flex flex-row align-items-left mt-3">
                    <p class="small text-muted mb-0">Дата: {{ props.post.published_at }}</p>
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class=" mx-auto w-50 mt-3">
                <base-image 
                :altContent="'Здесь должна быть картинка поста'" 
                :srcContent="post.image"
                class="rounded"
                ></base-image>
            </div>
            
            <p class="mt-5">{{ props.post.content }}</p>
        </div>
    </div>
</template>

<style scoped></style>
