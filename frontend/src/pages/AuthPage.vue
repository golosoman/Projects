<script>

export default {
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
                    <input type="email" id="form3Example2" class="form-control" />
                </div>

                <!-- Password input -->
                <div data-mdb-input-init class="form-outline mt-4 w-75 ">
                    <label class="form-label" for="form3Example3">Пароль</label>
                    <input type="password" id="form3Example3" class="form-control" />
                </div>

                <!-- Submit button -->
                <button data-mdb-ripple-init type="button" class="btn btn-dark btn-block mt-4 mb-4 w-50">Войти</button>
            </div>
        </form>
    </div>
  </div>
</template>

<style scoped></style>
