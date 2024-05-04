import {
    Controller,
    Get,
    Post,
    Body,
    Param,
    HttpCode,
    HttpStatus,
    Patch,
    Delete,
} from "@nestjs/common";
import { PostService } from "./post.service";
import { PostDto } from "./dto/post.dto";
import { CreatePostDto } from "./dto/create-post.dto";

@Controller("posts")
export class PostController {
    constructor(private postService: PostService) {}

    @Post()
    @HttpCode(HttpStatus.CREATED)
    async create(@Body() createPostDto: CreatePostDto) {
        // console.log(createPostDto);
        return this.postService.create(createPostDto);
    }

    @Get(":id")
    @HttpCode(HttpStatus.OK)
    async getOne(@Param("id") id: number): Promise<PostDto> {
        return this.postService.getOnePost(id);
    }

    @Get()
    @HttpCode(HttpStatus.OK)
    async getAll(): Promise<PostDto[]> {
      // console.log(123)
        return this.postService.getAllPosts();
    }

    @Patch(":id")
    @HttpCode(HttpStatus.OK)
    async update(@Param("id") id: number, @Body() updatePostDto: CreatePostDto): Promise<boolean> {
      return this.postService.updatePost(id, updatePostDto)
    }

    @Delete(":id")
    @HttpCode(HttpStatus.OK)
    async delete(@Param("id") id: number): Promise<boolean> {
      return this.postService.deletePost(id)
    }
}
