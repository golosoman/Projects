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
} from "@nestjs/common";
import { UserService } from "./user.service";
import { UserDto } from "./dto/user.dto";
import { CreateUserDto } from "./dto/create-user.dto";

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
    @HttpCode(HttpStatus.OK)
    async getAll(): Promise<UserDto[]> {
      // console.log(123)
        return this.userService.getAllUsers();
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
