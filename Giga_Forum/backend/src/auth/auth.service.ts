import { HttpException, HttpStatus, Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { CreateUserDto } from '../users/dto/create-users.dto';
import * as bcrypt from 'bcryptjs'
import { UserService } from '../users/users.service';
import { User } from '../users/users.model';
import { LoginUserDto } from 'src/users/dto/login-user.dto';
import { UserDto } from 'src/users/dto/users.dto';

@Injectable()
export class AuthService {
    constructor(private userService: UserService,
                private jwtService: JwtService) {}

    async login(userDto: LoginUserDto) {
        const user = await this.validateUser(userDto)
        return this.generateToken(user)
    }

    async registration(userDto: CreateUserDto) {
        const candidate = await this.userService.getUserByEmail(userDto.email);
        if (candidate) {
            throw new HttpException('Пользователь с таким email существует', HttpStatus.BAD_REQUEST);
        }
        const hashPassword = await bcrypt.hash(userDto.password, 5);
        const user = await this.userService.create({...userDto, password: hashPassword})
        console.log(user)
        return this.generateToken(user)
    }

    async getUserByToken(headers: Record<string, string>): Promise<UserDto> {
        const user = this.decodeJwtToken(
            headers["authorization"].split(" ")[1]
        );
        return this.userService.getOneUser(user.id)
    }

    private async generateToken(user: User) {
        const payload = {email: user.email, id: user.id, roles: user.roles}
        return {
            token: this.jwtService.sign(payload)
        }
    }

    public decodeJwtToken(token: string) {
        const payload = this.jwtService.verify(token);
        return payload;
    }

    private async validateUser(userDto: LoginUserDto) {
        const user = await this.userService.getUserByEmail(userDto.email);
        const passwordEquals = await bcrypt.compare(userDto.password, user.password);
        if (user && passwordEquals) {
            return user;
        }
        throw new UnauthorizedException({message: 'Некорректный email или пароль'})
    }
}
