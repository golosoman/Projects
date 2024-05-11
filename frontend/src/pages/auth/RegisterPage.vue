<script>
import { ref } from 'vue'
import {registerSchema} from '@/validator/registerSchema'
export default {
    setup() {
        let name = ref('')
        let email = ref('')
        let password = ref('')
        let password_confirmation = ref('')
        let is_admin = ref(null)
        let errorMessage = ref('')
        return { name, email, password, password_confirmation, is_admin, errorMessage }
    },
    methods: {
        register: async function () {
            let data = {
                name: this.name,
                email: this.email,
                password: this.password,
                is_admin: this.is_admin
            }
            try {
              await registerSchema.validate({
                name: this.name,
                email: this.email, 
                password: this.password, 
                confirmPassword: this.password_confirmation
              })
              this.$store
                .dispatch('register', data)
                .then(() => this.$router.push('/'))
                .catch((err) => {
                  console.log(err.message);
                  this.errorMessage = "Проверьте правильность введенных данных!"
                })
            } catch (error) {
              this.errorMessage = error.errors[0]
            }
            
        },
        clearMessage() {
      this.errorMessage = '';
    }
    }
}
</script>

<template>
   <alert-danger :message="errorMessage" @edit-message="clearMessage"></alert-danger>
    <div class="content row d-flex justify-content-center align-middle">
        <div class="w-50 p-3 border border-2 border-secondary rounded-5 mt-3 mb-3">
            <h1 class="text-center">Регистрация</h1>
            <form @submit.prevent>
                <div class="content row d-flex justify-content-center">
                    <base-input
                        labelText="Никнейм"
                        inputType="text"
                        inputPlaceholder="Введите никнейм:"
                        v-model="name"
                        class="mt-4 w-75"
                    ></base-input>

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

                    <base-input
                        labelText="Подтверждение пароля"
                        inputType="password"
                        inputPlaceholder="Подтвердите пароль:"
                        v-model="password_confirmation"
                        class="mt-4 w-75"
                    ></base-input>

                    <base-button @click="register" class="mt-4 mb-4 w-50"
                        >Зарегистрироваться</base-button
                    >
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped></style>
