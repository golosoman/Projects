package com.example.MedicalCalculators.dto.request.typeCalculator;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
@Schema(description = "Объект, включающий параметры для калькулятора расчета скорости внутривенного " +
        "капельного введения препарата")
public class RIDDCalculatorRequest extends BaseCalculatorRequest {
    @Schema(description = "Объем раствора в мл", example = "60")
    @Positive(message = "The value of the solution volume is strictly positive")
    private Double volumeOfSolution;

    @Schema(description = "Желаемое время введения препарата в минутах/часах", example = "30")
    @Positive(message = "The value of the desired drug administration time is strictly positive")
    private Double timeTaking;

    @Schema(description = "Время в минутах?", example = "true")
    private Boolean isMinute;
}
