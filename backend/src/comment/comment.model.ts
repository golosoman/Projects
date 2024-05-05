import { Table, DataType, Model, Column, HasMany, ForeignKey, CreatedAt } from "sequelize-typescript";
import { User } from "src/user/user.model";
import { Post } from "src/post/post.model";

interface CommentCreationAttrs{
    message: string;
    published_at: Date;
    author_id: number;
}

@Table({tableName: 'comments'})
export class Comment extends Model<Comment, CommentCreationAttrs>{
    @Column({type: DataType.INTEGER, unique: true, autoIncrement: true, primaryKey: true})
    id: number;

    @Column ({type: DataType.STRING, allowNull: false})
    message: string;

    @ForeignKey(() => User)
    @Column ({type: DataType.INTEGER, allowNull: false})
    author_id: number;

    @CreatedAt
    @Column
    published_at: Date;

    @HasMany(() => Post)
    posts: Post[];
}