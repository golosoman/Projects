import { Injectable } from "@nestjs/common";
import { CreateUserDto } from "./dto/create-user.dto";
import { User } from "./user.model";
import { UserDto } from "./dto/user.dto";
import { InjectModel } from "@nestjs/sequelize";

@Injectable()
export class UserService {
    constructor(@InjectModel(User) private userRepository: typeof User) {}

    async create(dto: CreateUserDto) {
        const user = await this.userRepository.create(dto);
        return user;
    }

    async getOneUser(id: number): Promise<UserDto> {
        const user = await this.userRepository.findByPk(id);
        return user;
    }

    async getAllUsers(): Promise<UserDto[]> {
        const users = await this.userRepository.findAll();
        return users;
    }

    async updateUser(id: number, dto: CreateUserDto): Promise<boolean>{
        const user = await this.userRepository.update(dto, {
            where: {
                id: id,
            },
        });
        console.log(user);
        return true;
    }

    async deleteUser(id: number): Promise<boolean>{
        const user = await this.userRepository.destroy({
            where: {
                id: id,
            }
        })
        console.log(user);
        return true;
    }
}
