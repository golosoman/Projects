import { Module } from "@nestjs/common";
import { SequelizeModule } from "@nestjs/sequelize";
import { ConfigModule } from "@nestjs/config";
import { Post } from "./post/post.model";
import { Comment } from "./comment/comment.model";
import { User } from "./user/user.model";
import { PostModule } from "./post/post.module";
import { UserModule } from "./user/user.module";
import { CommentModule } from "./comment/comment.module";

@Module({
    controllers: [],
    providers: [],
    imports: [
        ConfigModule.forRoot({
            envFilePath: `.env`
        }),
        SequelizeModule.forRoot({
            dialect: 'postgres',
            host: process.env.POSTGRES_HOST,
            port: Number(process.env.POSTGRES_PORT),
            username: process.env.POSTGRES_USER,
            password: process.env.POSTGRES_PASSWORD,
            database: process.env.POSTGRES_DB,
            models: [Post, Comment, User],
            autoLoadModels: true,
        }),
        PostModule,
        UserModule,
        CommentModule
    ]
})
export class AppModule {

}