<template>
  <alert-danger :message="errorMessage" @edit-message="clearMessage"></alert-danger>
    <loader v-if="isPostLoading || isCommentsLoading" />
    <div v-else class="content mt-3">
      
        <div class="row d-flex justify-content-center">
            <div class="setWidth">
                <post :post="post" />
            </div>
        </div>
        <div class="row d-flex justify-content-center mt-3 mb-3">
            <div class="col-md-8 col-lg-6">
                <div class="card shadow-0 border setCardBackColor">
                    <div v-if="isLoggedIn" class="form-outline mt-4 mx-4">
                        <base-input
                            labelText="Ваш комментарий"
                            inputType="text"
                            inputPlaceholder="Написать комментарий:"
                            v-model="message"
                            class="w-75"
                        ></base-input>
                        <base-button @click="postMessage" class="mt-3">Отправить</base-button>
                    </div>
                    <div v-else class="form-outline mt-4 mx-4">
                      <p>Прежде чем писать комментарии необходимо авторизоваться!</p>
                    </div>
                    <div class="card-body p-3">
                        <comments-list :commentsList="comments" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Post from '@/components/posts/Post.vue'
import CommentsList from '@/components/comments/CommentList.vue'
import Loader from '@/components/Loader.vue'
import { usePostById } from '@/hooks/post/usePostById'
import { useComments } from '@/hooks/useComments'
import { useRoute } from 'vue-router'
import { ref } from 'vue'
import { messageSchema } from '@/validator/messageSchema'
import axios from '@/axiosConfig'

export default {
    components: {
        Post,
        CommentsList,
        Loader
    },
    setup() {
        const route = useRoute()

        const { post, isPostLoading } = usePostById(route.params.id)
        console.log(post, 'postIdPage')

        const { comments, isCommentsLoading } = useComments(route.params.id)
        console.log(comments, 'PostIdPage')

        let message = ref('')
        let errorMessage = ref('')

        const postMessage = async () => {
            try {
                await messageSchema.validate({message: message.value})
                const response = await axios.post(`/posts/${route.params.id}/comments`, {
                    message: message.value
                })

                if (response.data) {
                    comments.value.unshift(response.data)
                    console.log(response.data)
                    message.value = ''
                }
                return response.data
            } catch (error) {
                errorMessage.value = error.errors[0];
            }
        }

        return { post, isPostLoading, comments, isCommentsLoading, postMessage, message, errorMessage }
    },
    methods:{
      clearMessage() {
      this.errorMessage = '';
    }
    },
    computed: {
        isLoggedIn: function () {
            return this.$store.getters.isLoggedIn
        }
    },
}
</script>

<style scoped>
.setWidth {
    width: 95%;
}
.setCardBackColor {
    background-color: #f0f2f5;
}
.alert-danger {
  z-index: 9999;
}
</style>
