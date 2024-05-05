import { Module } from "@nestjs/common";
import { CommentController } from "./comment.controller";
import { CommentService } from "./comment.service";
import { SequelizeModule } from "@nestjs/sequelize";
import { Post } from "../post/post.model";
import { Comment } from "src/comment/comment.model";
import { User } from "src/user/user.model";

@Module({
    controllers: [CommentController],
    providers: [CommentService],
    imports: [
        SequelizeModule.forFeature([Post, Comment, User])
    ]
})
export class CommentModule {}
