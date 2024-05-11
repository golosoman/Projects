package com.example.MedicalCalculators.exceptions.validation;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.util.Date;
import java.util.List;

@Getter
@RequiredArgsConstructor
@Schema(description = "Объект ответа сообщения об ошибке валидации")
public class ValidationErrorResponse {
    @Schema(description = "Код состояния http", example = "404")
    private final int statusCode;

    @Schema(description = "Дата и время, в которое произашла ошибка", example = "2024-04-22T17:01:56.160+04:00")
    private final Date timestamp;

    @Schema(description = "Cписок ошибок валидации", type = "array", implementation = Violation.class)
    private final List<Violation> violations;

}
