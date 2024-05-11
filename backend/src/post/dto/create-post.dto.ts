import { IsString } from "class-validator";

export class CreatePostDto {
    @IsString({ message: "Должно быть строкой" })
    title: string;

    @IsString({ message: "Должно быть строкой" })
    content: string;
}
