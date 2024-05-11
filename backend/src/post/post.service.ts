import { Injectable } from "@nestjs/common";
import { PostDto } from "./dto/post.dto";
import { Post } from "./post.model";
import { CreatePostDto } from "./dto/create-post.dto";
import { CreateCommentDto } from "../comment/dto/create-comment.dto";
import { InjectModel } from "@nestjs/sequelize";
import { HttpException, HttpStatus } from "@nestjs/common";
import { FilesService } from "src/files/files.service";
import { CommentService } from "src/comment/comment.service";
import { AddCommentDto } from "./dto/add-comment.dto";
import { Comment } from "src/comment/comment.model";
import { User } from "src/users/users.model";
import { AuthService } from "src/auth/auth.service";

@Injectable()
export class PostService {
    constructor(
        @InjectModel(Post)
        private postRepository: typeof Post,
        private fileService: FilesService,
        private commentsService: CommentService,
        private authService: AuthService
    ) {}

    async create(
        dto: CreatePostDto,
        image: any,
        headers: Record<string, string>
    ) {
        try {
            // console.log(headers['authorization'], "dasddadsa")
            const user = this.authService.decodeJwtToken(
                headers["authorization"].split(" ")[1]
            );
            const fileName = await this.fileService.createFile(image);
            console.log(user, fileName, dto);
            const post = await this.postRepository.create({
                ...dto,
                image: fileName,
                user_id: user.id,
            });
            return post;
        } catch (error) {
            throw new HttpException(
                {
                    status: HttpStatus.INTERNAL_SERVER_ERROR,
                    error: "Внутренняя ошибка сервера" + error.message,
                    time: Date.now(),
                },
                HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    async getOnePost(id: number): Promise<PostDto> {
        try {
            const post = await this.postRepository.findOne({
                where: { id: id, status: true },
                include: [
                    {
                        model: User,
                        attributes: {
                            exclude: ["id", "password"],
                        },
                    },
                ],
                attributes: { exclude: ["user_id"] },
            });
            if (!post) {
                throw new HttpException(
                    {
                        status: HttpStatus.NOT_FOUND,
                        error: "Пост не найден",
                        time: Date.now(),
                    },
                    HttpStatus.NOT_FOUND
                );
            }
            return post;
        } catch (error) {
            throw new HttpException(
                {
                    status: HttpStatus.INTERNAL_SERVER_ERROR,
                    error: "Внутренняя ошибка сервера",
                    time: Date.now(),
                },
                HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }


    async addComment(
        id: number,
        dto: AddCommentDto,
        headers: Record<string, string>
    ) {
        try {
            const user = this.authService.decodeJwtToken(
                headers["authorization"].split(" ")[1]
            );
            const post = await this.postRepository.findByPk(id);

            if (!post) {
                throw new HttpException(
                    {
                        status: HttpStatus.NOT_FOUND,
                        error: "Пост не найден",
                        time: Date.now(),
                    },
                    HttpStatus.NOT_FOUND
                );
            }
            const comment = await this.commentsService.create({
                ...dto,
                author_id: user.id,
                post_id: id,
            });

            await post.$add("comment", comment.id);
            return this.commentsService.getOneComment(comment.id);
        } catch (error) {
            throw new HttpException(
                {
                    status: HttpStatus.INTERNAL_SERVER_ERROR,
                    error: "Внутренняя ошибка сервера",
                    time: Date.now(),
                },
                HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    async getComments(id: number) {
        const post = await this.postRepository.findOne({
            where: { id: id },
            include: [
                {
                    model: Comment,
                    attributes: {
                        exclude: ["posts_id", "author_id"],
                    },
                    include: [
                        {
                            model: User,
                            attributes: {
                                exclude: ["id", "password"],
                            },
                        },
                    ],
                },
            ],
            order: [[{ model: Comment, as: 'comments' }, "updatedAt", "DESC"]],
        });

        if (!post) {
            throw new HttpException(
                {
                    status: HttpStatus.NOT_FOUND,
                    error: "Пост не найден",
                    time: Date.now(),
                },
                HttpStatus.NOT_FOUND
            );
        }

        return post.comments;
    }

    async getAllPosts(): Promise<PostDto[]> {
        try {
            const posts = await this.postRepository.findAll({
                where: { status: true },
                include: { all: true },
                order: [["updatedAt", "DESC"]],
            });
            return posts;
        } catch (error) {
            throw new HttpException(
                {
                    status: HttpStatus.INTERNAL_SERVER_ERROR,
                    error: "Внутренняя ошибка сервера",
                    time: Date.now(),
                },
                HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    async getAllFalseStatusPosts(): Promise<PostDto[]> {
        try {
            const posts = await this.postRepository.findAll({
                where: { status: false },
                include: { all: true },
                order: [["updatedAt", "DESC"]],
            });
            return posts;
        } catch (error) {
            throw new HttpException(
                {
                    status: HttpStatus.INTERNAL_SERVER_ERROR,
                    error: "Внутренняя ошибка сервера",
                    time: Date.now(),
                },
                HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    async updatePost(id: number, dto: CreatePostDto): Promise<boolean> {
        const post = await this.postRepository.update(dto, {
            where: {
                id: id,
            },
        });
        console.log(post);
        return true;
    }

    async deletePost(id: number): Promise<boolean> {
        const post = await this.postRepository.destroy({
            where: {
                id: id,
            },
        });
        console.log(post);
        return true;
    }
}
