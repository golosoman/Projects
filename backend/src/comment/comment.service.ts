import { Injectable } from "@nestjs/common";
import { CreateCommentDto } from "./dto/create-comment.dto";
import { PostDto } from "./dto/post.dto";
import { Post } from "./post.model";
import { InjectModel } from "@nestjs/sequelize";

@Injectable()
export class PostService {
    constructor(@InjectModel(Post) private postRepository: typeof Post) {}

    async create(dto: CreatePostDto) {
        const post = await this.postRepository.create(dto);
        return post;
    }

    async getOnePost(id: number): Promise<PostDto> {
        const post = await this.postRepository.findByPk(id);
        return post;
    }

    async getAllPosts(): Promise<PostDto[]> {
        const posts = await this.postRepository.findAll();
        return posts;
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
