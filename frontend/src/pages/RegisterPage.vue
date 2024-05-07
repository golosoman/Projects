<script>

export default {
    data(){
      return {
        name : "",
        email : "",
        password : "",
        password_confirmation : "",
        is_admin : null
      }
    },
    methods: {
      register: function () {
        let data = {
          name: this.name,
          email: this.email,
          password: this.password,
          is_admin: this.is_admin
        }
        this.$store.dispatch('register', data)
       .then(() => this.$router.push('/'))
       .catch(err => console.log(err))
      }
    }
}
</script>

<template>
  <div class="content row d-flex justify-content-center align-middle">
    
    <div class="w-50 p-3 border border-2 border-secondary rounded-5 mt-3 mb-3">
        <h1 class="text-center">Регистрации пользователя</h1>
        <form>
            <div class="content row d-flex justify-content-center">
                <!-- 2 column grid layout with text inputs for the first and last names -->
                <div data-mdb-input-init class="form-outline mt-3 w-75">
                    <label class="form-label" for="form3Example1">Никнейм</label>
                    <input type="text" id="form3Example1" class="form-control" />
                </div>

                <!-- Email input -->
                <div data-mdb-input-init class="form-outline mt-4 w-75">
                    <label class="form-label" for="form3Example2">Email адрес</label>
                    <input type="email" id="form3Example2" class="form-control" />
                </div>

                <!-- Password input -->
                <div data-mdb-input-init class="form-outline mt-4 w-75 ">
                    <label class="form-label" for="form3Example3">Пароль</label>
                    <input type="password" id="form3Example3" class="form-control" />
                </div>

                <div data-mdb-input-init class="form-outline mt-4 w-75">
                    <label class="form-label" for="form3Example4">Подтверждение пароля</label>
                    <input type="password" id="form3Example4" class="form-control" />
                </div>

                <!-- Submit button -->
                <button data-mdb-ripple-init type="button" class="btn btn-dark btn-block mt-4 mb-4 w-50">Зарегистрироваться</button>
            </div>
        </form>
    </div>
  </div>
</template>

<style scoped></style>
