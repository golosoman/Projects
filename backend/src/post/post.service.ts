import { Injectable, Post } from '@nestjs/common'
import { PostDto } from './dto/post.dto'
import { CreatePostDto } from './dto/create-post.dto'

@Injectable()
export class PostService {
    private readonly posts: PostDto[] = []

    create(post: CreatePostDto) {
        let a = new PostDto()
        a.authorId = post.authorId
        a.content = post.content
        a.title = post.title
        a.id = 1
        a.createdAt = new Date()
        this.posts.push(a)
    }

    getAllPosts(): PostDto[] {
        return this.posts
    }
}
