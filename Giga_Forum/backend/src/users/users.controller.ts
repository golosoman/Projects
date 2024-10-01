import {
    Controller,
    Get,
    Post,
    Body,
    Param,
    HttpCode,
    HttpStatus,
    Patch,
    Delete,
    UseGuards,
} from "@nestjs/common";
import { UserService } from "./users.service";
import { UserDto } from "./dto/users.dto";
import { CreateUserDto } from "./dto/create-users.dto";
import { JwtAuthGuard } from "src/auth/jwt-auth.guard";
import { Roles } from "../auth/roles-auth.decorator";
import { RolesGuard } from "../auth/roles.guard";
import { AddRoleDto } from "./dto/add-role.dto";

@Controller("users")
export class UserController {
    constructor(private userService: UserService) {}

    @Post()
    @HttpCode(HttpStatus.CREATED)
    async create(@Body() createPostDto: CreateUserDto) {
        // console.log(createPostDto);
        return this.userService.create(createPostDto);
    }

    @Get(":id")
    @HttpCode(HttpStatus.OK)
    async getOne(@Param("id") id: number): Promise<UserDto> {
        return this.userService.getOneUser(id);
    }

    @Get()
    @Roles("ADMIN")
    @UseGuards(RolesGuard)
    @HttpCode(HttpStatus.OK)
    async getAll(): Promise<UserDto[]> {
      // console.log(123)
        return this.userService.getAllUsers();
    }

    @Roles("ADMIN")
    @UseGuards(RolesGuard)
    @Post('/role')
    addRole(@Body() dto: AddRoleDto) {
        return this.userService.addRole(dto);
    }

    @Patch(":id")
    @HttpCode(HttpStatus.OK)
    async update(@Param("id") id: number, @Body() updateUserDto: CreateUserDto): Promise<boolean> {
      return this.userService.updateUser(id, updateUserDto)
    }

    @Delete(":id")
    @HttpCode(HttpStatus.OK)
    async delete(@Param("id") id: number): Promise<boolean> {
      return this.userService.deleteUser(id)
    }
}
