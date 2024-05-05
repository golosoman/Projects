import { Module } from "@nestjs/common";
import { UserService } from "./user.service";
import { UserController } from "./user.controller";
import { SequelizeModule } from "@nestjs/sequelize";
import { User } from "src/user/user.model";
import { Comment } from "src/comment/comment.model";
import { Post } from "src/post/post.model";

@Module({
    controllers: [UserController],
    providers: [UserService],
    imports: [
        SequelizeModule.forFeature([Post, Comment, User])
    ]
})

export class UserModule {}
