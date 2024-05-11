<template>
    <loader v-if="isUserLoading" />
    <div v-else class="container">
        <h1 class="mt-3 mb-3 text-center">Личный кабинет</h1>
        <div class="card mb-4">
            <div class="card-body ">
                <div class="row d-flex justify-content-center">
                    <div class="col-sm-3">
                        <p class="mb-0">Имя</p>
                    </div>
                    <div class="col-sm-9">
                        <p class="text-muted mb-0">{{ user.name }}</p>
                    </div>
                </div>
                <hr />
                <div class="row">
                    <div class="col-sm-3">
                        <p class="mb-0">Email</p>
                    </div>
                    <div class="col-sm-9">
                        <p class="text-muted mb-0">{{ user.email }}</p>
                    </div>
                </div>
                <hr />
                <div class="row">
                    <div class="col-sm-3">
                        <p class="mb-0">Репутация</p>
                    </div>
                    <div class="col-sm-9">
                        <p class="text-muted mb-0">{{ user.reputation }}</p>
                    </div>
                </div>
                <hr />
                <div class="row">
                    <div class="col-sm-3">
                        <p class="mb-0">Дата регистрации</p>
                    </div>
                    <div class="col-sm-9">
                        <p class="text-muted mb-0">{{ user.createdAt }}</p>
                    </div>
                </div>
                <hr />
                <div class="row">
                    <div class="col-sm-3">
                        <p class="mb-0">Роли:</p>
                    </div>
                    <div class="col-sm-9">
                        <ul>
                            <li v-for="role in user.roles" :key="role.value">
                                {{ role.value }} - {{ role.description }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useUser } from '@/hooks/useUser'
import Loader from '@/components/Loader.vue'
export default {
    components: { Loader },
    setup() {
        let { user, isUserLoading } = useUser()
        return {
            user,
            isUserLoading
        }
    }
}
</script>

<style scoped></style>
