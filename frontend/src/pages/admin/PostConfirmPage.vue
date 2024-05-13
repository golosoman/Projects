<script>
import PostList from '@/components/posts/PostList.vue'
import Loader from '@/components/Loader.vue'
import { usePosts } from '@/hooks/post/usePosts.js'
import useSortedPosts from '@/hooks/post/useSortedPosts.js'
import useSortedAndSearchedPosts from '@/hooks/post/useSortedAndSearchPosts.js'

export default {
    components: {
        PostList,
        Loader
    },
    setup() {
        const { posts, isPostsLoading } = usePosts(false)
        const { sortedPosts, selectedSort } = useSortedPosts(posts)
        const { searchQuery, sortedAndSearchedPosts } = useSortedAndSearchedPosts(sortedPosts)
        console.log(posts, 'PostConfirmPage')
        return { posts, isPostsLoading, searchQuery, sortedAndSearchedPosts, selectedSort }
    },
    methods: {
        removePost(id) {
      this.posts = this.posts.filter(p => p.id !== id)
    },
    }
}
</script>

<template>
    <div class="content row d-flex justify-content-center">
        <div class="content w-75 mt-2">
            <label class="form-label" for="formControlReadonly"><b>Поиск постов</b></label>
            <div class="form-outline" data-mdb-input-init>
                <input
                    v-model="searchQuery"
                    class="form-control-lg w-100"
                    id="formControlReadonly"
                    type="text"
                    value=""
                    placeholder="Поиск...."
                    aria-label="readonly input example"
                />
            </div>
        </div>
    </div>

    <loader v-if="isPostsLoading" />
    <div v-else class="content row d-flex justify-content-center">
        <div class="content w-75">
            <h2 v-if="posts.length === 0" class="mt-3">Постов для проверки нету!</h2>
            <post-list v-else :postList="sortedAndSearchedPosts" @del-post="removePost"/>
        </div>
    </div>
</template>

<style scoped></style>
