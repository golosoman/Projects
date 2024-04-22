package com.example.MedicalCalculators.dto.request.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.BaseCalculatorRequest;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
@Schema(description = "Объект запроса калькулятора индекса массы тела")
public class BMICalculatorRequest extends BaseCalculatorRequest {
    @Schema(description = "Вес человека в кг", example = "65")
    @Min(10)
    private Double weightPatient;
    @Min(1)
    @Max(300)
    @Schema(description = "Рост человека в см", example = "176")
    private Double height;
}
