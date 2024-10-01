package com.example.MedicalCalculators.exceptions.validation;

import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;

import java.util.Date;
import java.util.List;

@Getter
@RequiredArgsConstructor
@Schema(description = "Объект ответа сообщения об ошибке валидации")
public class ValidationErrorResponse {
    @Schema(description = "Код состояния http", example = "404")
    private final int statusCode;

    @Schema(description = "Дата и время, в которое произашла ошибка", example = "11-05-2024 19:28:57")
    @DateTimeFormat(pattern = "dd-MM-yyyy HH:mm:ss")
    @JsonFormat(pattern = "dd-MM-yyyy HH:mm:ss")
    private final Date timestamp;

    private final List<Violation> violations;
}
