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
import { CommentService } from "./comment.service";
import { CommentDto } from "./dto/comment.dto";
import { CreateCommentDto } from "./dto/create-comment.dto";

@Controller("comments")
export class CommentController {
    constructor(private commentService: CommentService) {}

    @Post()
    @HttpCode(HttpStatus.CREATED)
    async create(@Body() createCommentDto: CreateCommentDto) {
        // console.log(createCommentDto);
        return this.commentService.create(createCommentDto);
    }

    @Get(":id")
    @HttpCode(HttpStatus.OK)
    async getOne(@Param("id") id: number): Promise<CommentDto> {
        return this.commentService.getOneComment(id);
    }

    @Get()
    @HttpCode(HttpStatus.OK)
    async getAll(): Promise<CommentDto[]> {
      // console.log(123)
        return this.commentService.getAllComments();
    }

    @Patch(":id")
    @HttpCode(HttpStatus.OK)
    async update(@Param("id") id: number, @Body() updateCommentDto: CreateCommentDto): Promise<boolean> {
      return this.commentService.updateComment(id, updateCommentDto)
    }

    @Delete(":id")
    @HttpCode(HttpStatus.OK)
    async delete(@Param("id") id: number): Promise<boolean> {
      return this.commentService.deleteComment(id)
    }
}
