import { Table, DataType, Model, Column, HasMany, ForeignKey, CreatedAt, BelongsTo } from "sequelize-typescript";
import { User } from "src/users/users.model";
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

    @CreatedAt
    @Column
    published_at: Date;

    @ForeignKey(() => User)
    @Column ({type: DataType.INTEGER, allowNull: false})
    author_id: number;

    @BelongsTo(() => User)
    author: User

    @ForeignKey(() => Post)
    @Column ({type: DataType.INTEGER,  allowNull: true})
    posts_id: number;

    @BelongsTo(() => Post)
    post: Post
}