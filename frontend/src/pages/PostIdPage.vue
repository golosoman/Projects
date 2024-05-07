<template>
  <div class="content mt-3">
    <div class="row d-flex justify-content-center">
      <div class="setWidth">
        <post :post="post" />
      </div>
      
    </div>
    <div class="row d-flex justify-content-center mt-3">
      <div class="col-md-8 col-lg-6">
          <div class="card shadow-0 border" style="background-color: #f0f2f5;">
              <div class="card-body p-4">
                <comments-list :commentsList="comments" />
              </div>
          </div>
      </div>
      
    </div>
  </div>
</template>

<script>
import Post from '@/components/Post.vue'
import CommentsList from '@/components/CommentList.vue'
import { usePostById } from '@/hooks/post/usePostById';
import { useComments } from '@/hooks/useComments'
import { useRoute } from 'vue-router'

export default {
  components: {
    Post,
    CommentsList
  },
  setup() {
    const route = useRoute();

    const post = usePostById(route.params.id)
    console.log(route.params.id)
    const comments = useComments(route.params.id)
    console.log(comments)
    return { post, comments }
  }
}
</script>

<style scoped>
.setWidth{
  width: 95%;
}
</style>
