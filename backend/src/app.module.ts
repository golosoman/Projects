import { Module } from "@nestjs/common";
import { SequelizeModule } from "@nestjs/sequelize";
import { ConfigModule } from "@nestjs/config";
import { Post } from "./post/post.model";
import { Comment } from "./comment/comment.model";
import { User } from "./users/users.model";
import { PostModule } from "./post/post.module";
import { UserModule } from "./users/users.module";
import { CommentModule } from "./comment/comment.module";
import { AuthModule } from './auth/auth.module';
import { RolesModule } from './roles/roles.module';
import { UserRoles } from "./roles/user-roles.model";
import { Role } from "./roles/roles.model";
import { ServeStaticModule } from "@nestjs/serve-static";
import * as path from "path";

console.log(process.env.NODE_ENV)

@Module({
    controllers: [],
    providers: [],
    imports: [
        ConfigModule.forRoot({
            envFilePath: `.${process.env.NODE_ENV}.env`
        }),
        ServeStaticModule.forRoot({
            rootPath: path.resolve( __dirname, 'static'),
        }),
        SequelizeModule.forRoot({
            dialect: 'postgres',
            host: process.env.POSTGRES_HOST,
            port: Number(process.env.POSTGRES_PORT),
            username: process.env.POSTGRES_USER,
            password: process.env.POSTGRES_PASSWORD,
            database: process.env.POSTGRES_DB,
            models: [Post, Comment, User, UserRoles, Role],
            autoLoadModels: true,
        }),
        PostModule,
        UserModule,
        CommentModule,
        AuthModule,
        RolesModule
    ]
})
export class AppModule {

}