import { Table, DataType, Model, Column, HasMany } from "sequelize-typescript";
import { Comment } from "src/comment/comment.model";

interface UserCreationAttrs{
    nickname: string;
    email: string;
    reputation: number;
}

@Table({tableName: 'users'})
export class User extends Model<User, UserCreationAttrs>{
    @Column({type: DataType.INTEGER, unique: true, autoIncrement: true, primaryKey: true})
    id: number;

    @Column ({type: DataType.STRING, allowNull: false})
    name: string;

    @Column ({type: DataType.STRING, unique: true, allowNull: false})
    email: string;

    @Column ({type: DataType.INTEGER, allowNull: false})
    reputation: Date;

    @HasMany(() => Comment)
    posts: Comment[];
}