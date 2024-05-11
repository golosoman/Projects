<script>
import { ref } from 'vue'
import {authSchema} from '@/validator/authSchema'
export default {
    components: {},
    setup() {
        let email = ref('')
        let password = ref('')
        let errorMessage = ref('')
        return { email, password, errorMessage }
    },
    methods: {
        login: async function () {
            let email = this.email
            let password = this.password
            try {
              await authSchema.validate({email: email, password: password})
              this.$store
                .dispatch('login', { email, password })
                .then(() => this.$router.push('/'))
                .catch((err) => {
                  console.log(err.message);
                  this.errorMessage = "Неверный логин или пароль!"
                })
            } catch (error) {
              this.errorMessage = error.errors[0]
            }
        },
        clearMessage() {
      this.errorMessage = '';
    }
    },
}
</script>

<template>
  <alert-danger :message="errorMessage" @edit-message="clearMessage"></alert-danger>
    <div class="content row d-flex justify-content-center align-items-center mt-5">
        <div class="w-50 p-3 border border-2 border-secondary rounded-5 mt-3 mb-3">
            <h1 class="text-center">Авторизация</h1>

            <form @submit.prevent>
                <div class="content row d-flex justify-content-center">
                    <base-input
                        labelText="Email адрес"
                        inputType="email"
                        inputPlaceholder="Введите еmail адрес:"
                        v-model="email"
                        class="mt-4 w-75"
                    ></base-input>

                    <base-input
                        labelText="Пароль"
                        inputType="password"
                        inputPlaceholder="Введите пароль:"
                        v-model="password"
                        class="mt-4 w-75"
                    ></base-input>

                    <base-button
                        @click="login"
                        class="mt-4 mb-4 w-50"
                        >Войти</base-button
                    >
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped></style>
