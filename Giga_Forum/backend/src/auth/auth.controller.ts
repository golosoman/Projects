import {Body, Controller, Get, Post, Headers} from '@nestjs/common';
import { CreateUserDto } from 'src/users/dto/create-users.dto';
import { AuthService } from './auth.service';
import { LoginUserDto } from 'src/users/dto/login-user.dto';

@Controller('auth')
export class AuthController {

    constructor(private authService: AuthService) {}

    @Post('/login')
    login(@Body() userDto: LoginUserDto) {
        return this.authService.login(userDto)
    }

    @Get("/login/user")
    getUser(@Headers() headers: Record<string, string>){
        return this.authService.getUserByToken(headers)
    }

    @Post('/registration')
    registration(@Body() userDto: CreateUserDto) {
        return this.authService.registration(userDto)
    }
}
