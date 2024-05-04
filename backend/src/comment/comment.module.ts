import { Module } from "@nestjs/common";
import { PostController } from "../post/post.controller";
import { PostService } from "../post/post.service";
import { SequelizeModule } from "@nestjs/sequelize";
import { Post } from "../post/post.model";
import { Comment } from "src/comment/comment.model";
import { User } from "src/user/user.model";

@Module({
    controllers: [PostController],
    providers: [PostService],
    imports: [
        SequelizeModule.forFeature([Post, Comment, User])
    ]
})
export class PostModule {}
