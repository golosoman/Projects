package com.example.MedicalCalculators.exceptions.api;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Getter
@Setter
@AllArgsConstructor
@Schema(description = "Объект сообщения об ошибке")
public class ErrorMessage {
    @Schema(description = "Код состояния http", example = "404")
    private int statusCode;

    @Schema(description = "Дата и время, в которое произашла ошибка", example = "2024-04-22T17:01:56.160+04:00")
    private Date timestamp;

    @Schema(description = "Сообщение об ошибке", example = "Калькулятор с идентификатором 5 не найден")
    private String message;

    @Schema(description = "Описание запроса", example = "Resolved [com.example.MedicalCalculators." +
            "exceptions.NotFoundException: Калькулятор с идентификатором 5 не найден]")
    private String description;
}
