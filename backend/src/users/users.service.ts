import { HttpException, HttpStatus, Injectable } from "@nestjs/common";
import { CreateUserDto } from "./dto/create-users.dto";
import { User } from "./users.model";
import { UserDto } from "./dto/users.dto";
import { InjectModel } from "@nestjs/sequelize";
import { RolesService } from "../roles/roles.service";
import { AddRoleDto } from "./dto/add-role.dto";
import { Role } from "src/roles/roles.model";
import { AuthService } from "src/auth/auth.service";

@Injectable()
export class UserService {
    constructor(@InjectModel(User) 
        private userRepository: typeof User, 
        private roleService: RolesService
    ) {}

    async create(dto: CreateUserDto) {
        const user = await this.userRepository.create(dto);
        const role = await this.roleService.getRoleByValue("ADMIN")
        await user.$set('roles', [role.id])
        user.roles = [role]
        return user;
    }

    async getOneUser(id: number): Promise<UserDto> {
        const user = await this.userRepository.findOne({
            where: { id: id },
                include: [
                    {
                        model: Role,
                        attributes: {
                            exclude: ["id", "createdAt", "updatedAt", "UserRoles"],
                        },
                    },
                ],
                attributes: { exclude: ["password", "updatedAt"] },
        });
        return user;
    }

    async getAllUsers(): Promise<UserDto[]> {
        const users = await this.userRepository.findAll({include: {all: true}});
        return users;
    }

    async getUserByEmail(email: string) {
        const user = await this.userRepository.findOne({where: {email}, include: {all: true}})
        return user;
    }

    async addRole(dto: AddRoleDto) {
        const user = await this.userRepository.findByPk(dto.userId);
        const role = await this.roleService.getRoleByValue(dto.value);
        if (role && user) {
            await user.$add('role', role.id);
            return dto;
        }
        throw new HttpException('Пользователь или роль не найдены', HttpStatus.NOT_FOUND);
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
