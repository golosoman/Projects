import { Controller, Get, Post, Body } from '@nestjs/common'
import { PostService } from './post.service'
import { PostDto } from './dto/post.dto'
import { CreatePostDto } from './dto/create-post.dto'

@Controller('post')
export class PostController {
  constructor(private postService: PostService) {}

  @Post()
  async create(@Body() createPostDto: CreatePostDto) {
    this.postService.create(createPostDto)
  }

  @Get()
  async getAllPosts(): Promise<PostDto[]> {
    return this.postService.getAllPosts()
  }
}
