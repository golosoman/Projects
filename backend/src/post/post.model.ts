import { Table, DataType, Model, Column, HasMany, ForeignKey, CreatedAt } from "sequelize-typescript";
import { Comment } from "../comment/comment.model";

interface PostCreationAttrs{
    title: string;
    content: string;
    published_at: Date;
    status: boolean;
}

@Table({tableName: 'posts'})
export class Post extends Model<Post, PostCreationAttrs>{
    @Column({type: DataType.INTEGER, unique: true, autoIncrement: true, primaryKey: true})
    id: number;

    @Column ({type: DataType.STRING, allowNull: false})
    title: string;

    @Column ({type: DataType.STRING, allowNull: false})
    content: string;

    @Column ({type: DataType.BOOLEAN, allowNull: false})
    status: boolean;

    @CreatedAt
    @Column
    published_at: Date;

    @ForeignKey(() => Comment)
    @Column ({type: DataType.INTEGER,  allowNull: true})
    comments_id: number;
    
    // @HasMany(() => Comment)
    // posts: Comment[];
}