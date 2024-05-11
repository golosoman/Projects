import { Injectable } from "@nestjs/common";
import { CreateCommentDto } from "./dto/create-comment.dto";
import { CommentDto } from "./dto/comment.dto";
import { Comment } from "./comment.model";
import { InjectModel } from "@nestjs/sequelize";
import { User } from "src/users/users.model";

@Injectable()
export class CommentService {
    constructor(@InjectModel(Comment) private commentRepository: typeof Comment) {}

    async create(dto: CreateCommentDto) {
        const comment = await this.commentRepository.create(dto);
        return comment;
    }

    public async getOneComment(id: number): Promise<CommentDto> {
        const comment = await this.commentRepository.findOne({
            where: {id:id}, 
            include: [{
                model: User,
                attributes: {
                exclude: ["id", "password"],
                },
            }],
            attributes: { exclude: ["author_id", "posts_id"]}
        });
        return comment;
    }

    async getAllComments(): Promise<CommentDto[]> {
        const comments = await this.commentRepository.findAll();
        return comments;
    }

    async getAllCommentsByPostId(): Promise<CommentDto[]> {
        const comments = await this.commentRepository.findAll();
        return comments;
    }

    async updateComment(id: number, dto: CreateCommentDto): Promise<boolean>{
        const comment = await this.commentRepository.update(dto, {
            where: {
                id: id,
            },
        });
        console.log(comment);
        return true;
    }

    async deleteComment(id: number): Promise<boolean>{
        const comment = await this.commentRepository.destroy({
            where: {
                id: id,
            }
        })
        console.log(comment);
        return true;
    }
}
