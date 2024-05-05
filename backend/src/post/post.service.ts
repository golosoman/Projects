import { Injectable } from "@nestjs/common";
import { PostDto } from "./dto/post.dto";
import { Post } from "./post.model";
import { CreatePostDto } from "./dto/create-post.dto";
import { InjectModel } from "@nestjs/sequelize";
import { HttpException, HttpStatus } from '@nestjs/common'

@Injectable()
export class PostService {
    constructor(@InjectModel(Post) private postRepository: typeof Post) {}

    async create(dto: CreatePostDto) {
        const post = await this.postRepository.create(dto);
        return post;
    }

    async getOnePost(id: number): Promise<PostDto> {
        try {
            const post = await this.postRepository.findByPk(id);
            if (!post){
                throw new HttpException({
                    status: HttpStatus.NOT_FOUND,
                    error: "Пост не найден",
                    time: Date.now()
                }, HttpStatus.NOT_FOUND)
            }
            return post;
        } catch (error) {
            throw new HttpException({
                status: HttpStatus.INTERNAL_SERVER_ERROR,
                error: "Внутренняя ошибка сервера",
                time: Date.now()
            }, HttpStatus.INTERNAL_SERVER_ERROR)
        }
    }

    async getAllPosts(): Promise<PostDto[]> {
        try {
            const posts = await this.postRepository.findAll();
            return posts;
        } catch (error) {
            throw new HttpException({
                status: HttpStatus.INTERNAL_SERVER_ERROR,
                error: "Внутренняя ошибка сервера",
                time: Date.now()
            }, HttpStatus.INTERNAL_SERVER_ERROR)
        }
        
    }

    async updatePost(id: number, dto: CreatePostDto): Promise<boolean>{
        const post = await this.postRepository.update(dto, {
            where: {
                id: id,
            },
        });
        console.log(post);
        return true;
    }

    async deletePost(id: number): Promise<boolean>{
        const post = await this.postRepository.destroy({
            where: {
                id: id,
            }
        })
        console.log(post);
        return true;
    }
}
