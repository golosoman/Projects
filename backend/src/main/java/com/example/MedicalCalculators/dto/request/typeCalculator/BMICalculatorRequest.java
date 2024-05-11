package com.example.MedicalCalculators.dto.request.typeCalculator;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
@Schema(description = "Объект, включающий параметры для калькулятора индекса массы тела")
public class BMICalculatorRequest extends BaseCalculatorRequest {
    @Schema(description = "Вес человека в кг", example = "65")
    @Min(value = 10, message = "Минимальный вес составляет 10 кг")
    private Double weightPatient;

    @Schema(description = "Рост человека в см", example = "176")
    @Positive(message = "Значение роста является строго положительным")
    @Max(value = 300, message = "Рост не должен превышать 300 см")
    private Double height;
}
