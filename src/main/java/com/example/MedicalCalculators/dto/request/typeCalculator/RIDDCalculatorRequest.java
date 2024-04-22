package com.example.MedicalCalculators.dto.request.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.BaseCalculatorRequest;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
@Schema(description = "Объект запроса калькулятора для расчета скорости внутривенного " +
        "капельного введения препарата")
public class RIDDCalculatorRequest extends BaseCalculatorRequest {
    @Schema(description = "Объем раствора в мл", example = "60")
    private Double volumeOfSolution;
    @Schema(description = "Желаемое время введения препарата в минутах", example = "30")
    private Double timeTaking;
}
