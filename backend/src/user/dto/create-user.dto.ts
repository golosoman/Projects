import { ApiProperty } from "@nestjs/swagger";

export class CreateUserDto{
    readonly name:string;
    @ApiProperty({example: 'userExample@mail.ru', description: 'Почтовый адрес'})
    readonly email:string;
    @ApiProperty({example: '1234567890', description: 'Пароль'})
    readonly password: string;
}