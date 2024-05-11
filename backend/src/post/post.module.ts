import { Module } from "@nestjs/common";
import { PostController } from "./post.controller";
import { PostService } from "./post.service";
import { SequelizeModule } from "@nestjs/sequelize";
import { Post } from "./post.model";
import { Comment } from "../comment/comment.model";
import { User } from "../users/users.model";
import { FilesModule } from "../files/files.module";
import { CommentModule } from "src/comment/comment.module";
import { AuthModule } from "src/auth/auth.module";

@Module({
    controllers: [PostController],
    providers: [PostService],
    imports: [
        SequelizeModule.forFeature([Post, Comment, User]),
        FilesModule,
        CommentModule,
        AuthModule,
    ],
})
export class PostModule {}
