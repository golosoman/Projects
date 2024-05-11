package com.example.MedicalCalculators.dto.request.typeCalculator;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
@Schema(description = "Объект, включающий параметры для калькулятора расчета скорости инфузии " +
        "препарата через линеомат (скорость титрования)")
public class TitrationCalculatorRequest extends BaseCalculatorRequest {
    @Schema(description = "Вес человека в кг", example = "65")
    @Positive(message = "Значение веса строго положительное")
    private Double weightPatient;

    @Schema(description = "Дозировка препарата в мкг*кг/мин или мл/час", example = "2")
    @Positive(message = "Дозировка препарата строго положительная")
    private Double dosage;

    @Schema(description = "Количество препарата в мг", example = "10")
    @Positive(message = "Значение количества препарата является строго положительным")
    private Double amountOfDrug;

    @Schema(description = "Общий объем раствора в мл", example = "50")
    @Positive(message = "Значение общего объема раствора является строго положительным")
    private Double volumeOfSolution;

    @Schema(description = "Дозировка в мл/час?", example = "true")
    private Boolean isMlInHour;
}
