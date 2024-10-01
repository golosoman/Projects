import { Table, DataType, Model, Column, HasMany, BelongsToMany } from "sequelize-typescript";
import { Comment } from "../comment/comment.model";
import { Post } from "../post/post.model";
import { Role } from "../roles/roles.model";
import { UserRoles } from "../roles/user-roles.model";

interface UserCreationAttrs{
    name: string;
    email: string;
    password: string;
}

@Table({tableName: 'users'})
export class User extends Model<User, UserCreationAttrs>{
    @Column({type: DataType.INTEGER, unique: true, autoIncrement: true, primaryKey: true})
    id: number;

    @Column ({type: DataType.STRING, allowNull: false})
    name: string;

    @Column ({type: DataType.STRING, unique: true, allowNull: false})
    email: string;

    @Column({type: DataType.STRING, allowNull: false})
    password: string;

    @Column ({type: DataType.INTEGER, allowNull: false, defaultValue: 0})
    reputation: number;

    @HasMany(() => Comment)
    comments: Comment[];

    @HasMany(() => Post)
    posts: Post[];

    @BelongsToMany(() => Role, () => UserRoles)
    roles: Role[];
}