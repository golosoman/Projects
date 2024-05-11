package com.example.MedicalCalculators.exceptions.validation;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
@Schema(description = "Объект ошибки валидации")
public class Violation {
    @Schema(description = "Название поля, в котором произошла ошибка",
            example = "getBMIResult.calculatorRequest.weightPatient")
    private final String fieldName;

    @Schema(description = "Название ошибки",
            example = "Минимальный вес составляет 10 кг")
    private final String message;

}
