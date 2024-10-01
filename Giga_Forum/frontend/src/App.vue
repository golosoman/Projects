<script>
import Navbar from "@/components/Navbar.vue";
// import Loader from "@/components/Loader.vue";

export default{
  components: {
    Navbar,
    // Loader
  },
}

// import { onMounted, ref } from 'vue'
// import PostList from './components/PostList.vue'

// import commentsList from './data/comments.json'
// import userList from './data/users.json'

// let comments = ref([])
// let users = ref([])

// onMounted(() => {
//   comments.value = commentsList
//   users.value = userList
// })
</script>

<template>
  <div class="content">
    <navbar></navbar>
    <router-view />
    <!-- <loader></loader> -->
  </div>
</template>

<style scoped>
</style>
