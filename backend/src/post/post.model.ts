import {
    Table,
    DataType,
    Model,
    Column,
    HasMany,
    ForeignKey,
    CreatedAt,
    BelongsTo,
} from "sequelize-typescript";
import { Comment } from "../comment/comment.model";
import { User } from "../users/users.model";

interface PostCreationAttrs {
    title: string;
    content: string;
    user_id: number;
    image: string;
}

@Table({ tableName: "posts" })
export class Post extends Model<Post, PostCreationAttrs> {
    @Column({
        type: DataType.INTEGER,
        unique: true,
        autoIncrement: true,
        primaryKey: true,
    })
    id: number;

    @Column({ type: DataType.STRING, allowNull: false })
    title: string;

    @Column({ type: DataType.STRING, allowNull: false })
    content: string;

    @Column({ type: DataType.BOOLEAN, allowNull: false, defaultValue: false })
    status: boolean;

    @Column({ type: DataType.STRING })
    image: string;

    @CreatedAt
    @Column
    published_at: Date;

    @ForeignKey(() => User)
    @Column({ type: DataType.INTEGER })
    user_id: number;

    @BelongsTo(() => User)
    author: User;

    @HasMany(() => Comment)
    comments: Comment[];
}
