import { Module, forwardRef } from "@nestjs/common";
import { UserService } from "./users.service";
import { UserController } from "./users.controller";
import { SequelizeModule } from "@nestjs/sequelize";
import { User } from "./users.model";
import { Comment } from "../comment/comment.model";
import { Post } from "../post/post.model";
import { UserRoles } from "../roles/user-roles.model";
import { RolesModule } from "../roles/roles.module";
import { AuthModule } from "../auth/auth.module";
import { AuthService } from "src/auth/auth.service";
import { RolesService } from "src/roles/roles.service";

@Module({
    controllers: [UserController],
    providers: [UserService],
    imports: [
        forwardRef(() => AuthModule),
        SequelizeModule.forFeature([Post, Comment, User, UserRoles]),
        RolesModule,
    ],
    exports: [UserService]
})

export class UserModule {}
