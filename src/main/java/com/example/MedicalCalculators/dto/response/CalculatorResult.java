package com.example.MedicalCalculators.dto.response;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
@Schema(description = "Объект результата вычисления калькулятора", contentMediaType = "application/json")
public class CalculatorResult {
    @Schema(description = "Результат", example = "20,984")
    String result;
}
