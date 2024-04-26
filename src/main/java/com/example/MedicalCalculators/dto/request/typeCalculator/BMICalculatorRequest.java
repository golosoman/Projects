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
    @Min(value = 10, message = "The minimum weight value is 10 kg")
    private Double weightPatient;

    @Schema(description = "Рост человека в см", example = "176")
    @Positive(message = "The growth value is strictly positive")
    @Max(value = 300, message = "The height cannot exceed 300 cm")
    private Double height;
}
