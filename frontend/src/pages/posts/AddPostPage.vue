<template>
    <!-- <div class="alert alert-success" role="alert">
        A simple success alert with <a href="#" class="alert-link">an example link</a>. Give it a click if you like.
    </div> -->
    <alert-danger :message="errorMessage" @edit-message="clearMessage"></alert-danger>
    <div class="row d-flex justify-content-center">
        <div class="content p-3 mt-3 w-75">
            <div class="border border-secondary rounded-3 p-3">
                <form @submit.prevent>
                    <b><base-input
                        labelText="Заголовок поста"
                        inputType="text"
                        inputPlaceholder="Введите заголовок поста:"
                        v-model="title"
                        class="mt-4  mb-4"
                    ></base-input></b>
                    

                    <div data-mdb-input-init class="form-outline mb-4">
                        <label class="form-label" for="form4Example3"
                            ><b>Содержимое поста</b></label
                        >
                        <textarea
                            class="form-control"
                            id="form4Example3"
                            rows="5"
                            placeholder="Введите содержимое поста:"
                            v-model="content"
                        ></textarea>
                    </div>

                    <div class="mb-3">
                        <label class="form-label" for="customFile"><b>Изображение поста</b></label>
                        <input
                            type="file"
                            ref="fileDOM"
                            class="form-control"
                            id="customFile"
                            @change="onChange"
                        />
                    </div>

                    <base-button @click="postData" class="mb-4">Отправить</base-button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'
import { postSchema } from '@/validator/postSchema'
import axios from '@/axiosConfig'

export default {
    components: {},
    setup() {
        let title = ref('')
        let content = ref('')
        let file = ref(null)
        let fileDOM = ref(null)
        let errorMessage = ref('')

        const postData = async () => {
            try {
                await postSchema.validate({title: title.value, content: content.value, image: file.value})
                let formData = new FormData()
                formData.append('title', title.value)
                formData.append('content', content.value)
                formData.append('image', file.value, file.value.name)

                console.log(content.value)

                const response = await axios.post('/posts', formData)
                if (response.data) {
                    title.value = ''
                    content.value = ''
                    resetFileInput()
                    return true
                } else {
                    console.log('Что-то пошло не так')
                    return false
                }
            } catch (error) {
                errorMessage.value = error.errors[0]
            }
        }

        const resetFileInput = () => {
            const newFileInput = document.createElement('input')
            newFileInput.type = 'file'
            newFileInput.id = 'customFile'
            newFileInput.name = 'customFile'
            newFileInput.classList.add('form-control')
            newFileInput.addEventListener('change', onChange)
            deleteFile(newFileInput)
        }

        const deleteFile = (newFileInput) => {
            const oldFileInput = fileDOM.value
            oldFileInput.parentNode.replaceChild(newFileInput, oldFileInput)
        }

        const onChange = (e) => {
            file.value = e.target.files[0]
            console.log(file.value)
        }

        return { title, content, file, fileDOM, postData, onChange, errorMessage }
    },
    methods:{
        clearMessage() {
      this.errorMessage = '';
    }
    }
}
</script>
