<!-- <script setup>
import {ref} from 'vue';
import axios from '@/axiosConfig';

let token = ref(null);
let email = ref("");
let password = ref("");

const login = async(body) => {
    console.log(body)
    try {
        const response = await axios.post('auth/login', body);
        token.value = response.data.token;
        console.log(token.value);
        return token
    } catch (error) {
        console.log("Отвалилась авторизация")
    }
}
</script> -->

<script>
  export default {
    data(){
      return {
        email : "",
        password : ""
      }
    },
    methods: {
      login: function () {
        let email = this.email 
        let password = this.password
        this.$store.dispatch('login', { email, password })
       .then(() => this.$router.push('/'))
       .catch(err => console.log(err))
      }
    }
  }
</script>

<template>
  <div class="content row d-flex justify-content-center align-items-center mt-5">
    
    <div class="w-50 p-3 border border-2 border-secondary rounded-5 mt-3 mb-3">
        <h1 class="text-center">Авторизация</h1>
        
        <form>
            <div class="content row d-flex justify-content-center">
                <!-- Email input -->
                <div data-mdb-input-init class="form-outline mt-4 w-75">
                    <label class="form-label" for="form3Example2">Email адрес</label>
                    <input type="email" id="form3Example2" class="form-control" v-model="email"/>
                </div>

                <!-- Password input -->
                <div data-mdb-input-init class="form-outline mt-4 w-75 ">
                    <label class="form-label" for="form3Example3" >Пароль</label>
                    <input type="password" id="form3Example3" class="form-control" v-model="password"/>
                </div>

                <!-- Submit button -->
                <button data-mdb-ripple-init type="button" @click="login({email: email, password: password})" class="btn btn-dark btn-block mt-4 mb-4 w-50">Войти</button>
            </div>
        </form>
    </div>
  </div>
</template>

<style scoped></style>
