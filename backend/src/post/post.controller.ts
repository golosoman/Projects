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
    UploadedFile,
    UseInterceptors,
    UseGuards,
    Req,
    Headers,
    Query,
} from "@nestjs/common";
import { PostService } from "./post.service";
import { PostDto } from "./dto/post.dto";
import { CreatePostDto } from "./dto/create-post.dto";
import { FileInterceptor } from "@nestjs/platform-express";
import { CreateCommentDto } from "src/comment/dto/create-comment.dto";
import { AddCommentDto } from "./dto/add-comment.dto";
import { Roles } from "src/auth/roles-auth.decorator";
import { RolesGuard } from "src/auth/roles.guard";

@Controller("posts")
export class PostController {
    constructor(private postService: PostService) {}

    @Post()
    @Roles("USER", "ADMIN")
    @UseGuards(RolesGuard)
    @UseInterceptors(FileInterceptor("image"))
    createPost(
        @Body() dto: CreatePostDto,
        @UploadedFile() image: any,
        @Headers() headers: Record<string, string>
    ) {
        console.log(image);
        return this.postService.create(dto, image, headers);
    }

    @Get(":id")
    @HttpCode(HttpStatus.OK)
    async getOne(@Param("id") id: number): Promise<PostDto> {
        return this.postService.getOnePost(id);
    }


    @Post(":id/comments")
    @Roles("USER", "ADMIN")
    @UseGuards(RolesGuard)
    @HttpCode(HttpStatus.OK)
    async addComment(
        @Param("id") id: number,
        @Body() dto: AddCommentDto,
        @Headers() headers: Record<string, string>
    ): Promise<AddCommentDto> {
        return this.postService.addComment(id, dto, headers);
    }

    @Get(":id/comments")
    @HttpCode(HttpStatus.OK)
    async getComments(@Param("id") id: number) {
        return this.postService.getComments(id);
    }

    @Get()
    @HttpCode(HttpStatus.OK)
    async getAll(@Query() query: any): Promise<PostDto[]> {
        // console.log(123)
        return this.postService.getAllPosts(query);
    }

    @Patch(":id/confirm")
    @HttpCode(HttpStatus.OK)
    async postConfirm(
        @Param("id") id: number,
    ){
        return this.postService.setStatusTrue(id);
    }

    @Patch(":id")
    @HttpCode(HttpStatus.OK)
    async update(
        @Param("id") id: number,
        @Body() updatePostDto: CreatePostDto
    ): Promise<boolean> {
        return this.postService.updatePost(id, updatePostDto);
    }

    @Delete(":id")
    @HttpCode(HttpStatus.OK)
    async delete(@Param("id") id: number): Promise<boolean> {
        return this.postService.deletePost(id);
    }
}
