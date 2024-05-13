<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="menu">
        <div id="menuHolder" :class="menuHolderClass">
            <div role="navigation" class="sticky-top border-bottom border-top" id="mainNavigation">
                <div class="flexMain">
                    <div class="flex2">
                        <button
                            class="whiteLink siteLink"
                            style="border-right: 1px solid #eaeaea"
                            @click="menuToggle"
                        >
                            <i class="fas fa-bars me-2"></i>Меню
                        </button>
                    </div>
                    <div class="flex3 text-center" id="siteBrand">ГигаФорум</div>

                    <div class="flex2 text-end d-block d-md-none">
                        <button class="whiteLink siteLink"><i class="fas fa-search"></i></button>
                    </div>

                    <div v-if="isLoggedIn" class="flex2 text-end d-none d-md-block">
                        <button @click="$router.push('/posts/add')" class="whiteLink siteLink">
                            Добавить пост
                        </button>
                        <button @click="logout" class="redLink siteLink">Выйти из аккаунта</button>
                    </div>

                    <div v-else class="flex2 text-end d-none d-md-block">
                        <button @click="$router.push('/auth/register')" class="whiteLink siteLink">
                            Зарегестрироваться
                        </button>
                        <button @click="$router.push('/auth/login')" class="blackLink siteLink">
                            Войти
                        </button>
                    </div>
                </div>
            </div>

            <div id="menuDrawer">
                <div class="p-4 border-bottom">
                    <div class="row">
                        <div class="col">
                            <h4>Панель навигации</h4>
                        </div>
                        <div class="col text-end">
                            <i class="fas fa-times" role="btn" @click="menuToggle"></i>
                        </div>
                    </div>
                </div>
                <div>
                    <a @click="$router.push('/auth/login/cabinet')" class="nav-menu-item"
                        ><i class="fas fa-search me-3"></i>Личный кабинет</a
                    >
                    <a @click="$router.push('/')" class="nav-menu-item"
                        ><i class="fas fa-home me-3"></i>Посты</a
                    >
                    <a v-if="isLoggedIn" @click="$router.push('/posts/confirm')" class="nav-menu-item"
                        ><i class="fas fa-home me-3"></i>Модерация</a
                    >
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'
export default {
    setup() {
        let menuHolderClass = ref('')
        const menuToggle = () => {
            if (menuHolderClass.value === 'drawMenu') menuHolderClass.value = ''
            else menuHolderClass.value = 'drawMenu'
        }
        return { menuHolderClass, menuToggle }
    },
    computed: {
        isLoggedIn: function () {
            return this.$store.getters.isLoggedIn
        }
    },
    methods: {
        logout: function () {
            this.$store.dispatch('logout').then(() => {
                this.$router.push('/auth/login')
            })
        }
    }
}
</script>

<style scoped>
.flexMain {
    display: flex;
    align-items: center;
}
.flex1 {
    flex: 1;
}
.flex2 {
    flex: 2;
}
.flex3 {
    flex: 3;
}

button.siteLink {
    margin-left: -5px;
    border: none;
    padding: 24px;
    display: inline-block;
    min-width: 115px;
}
.whiteLink {
    background: #fff;
}
.whiteLink:active {
    background: #000;
    color: #fff;
}
.blackLink {
    color: #fff;
    background: #232323;
    transition: all 300ms linear;
}

.redLink {
    color: #fff;
    background: #f84646;
    transition: all 300ms linear;
}
.redLink:active {
    color: #ff0000;
    background: #fff;
}

.blackLink:active {
    color: #000;
    background: #fff;
}
#siteBrand {
    font-family: impact;
    letter-spacing: -1px;
    font-size: 32px;
    color: #252525;
    line-height: 1em;
}
#menuDrawer {
    background: #fff;
    position: fixed;
    height: 100vh;
    overflow: auto;
    z-index: 12312;
    top: 0;
    left: 0;
    border-right: 1px solid #eaeaea;
    min-width: 25%;
    max-width: 320px;
    width: 100%;
    transform: translateX(-100%);
    transition: transform 200ms linear;
}
#mainNavigation {
    transition: transform 200ms linear;
    background: #fff;
}
.drawMenu > #menuDrawer {
    transform: translateX(0%);
}
.drawMenu > #mainNavigation {
    transform: translateX(25%);
}
.fa-times {
    cursor: pointer;
}
a.nav-menu-item:hover {
    margin-left: 2px;
    border-left: 10px solid black;
}
a.nav-menu-item {
    transition: border 200ms linear;
    text-decoration: none;
    display: block;
    padding: 18px;
    padding-left: 32px;
    border-bottom: 1px solid #eaeaea;
    font-weight: bold;
    color: #343434;
}
select.noStyle {
    border: none;
    outline: none;
}
</style>
