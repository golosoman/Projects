package com.example.MedicalCalculators.dto.request.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.BaseCalculatorRequest;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
@Schema(description = "Объект запроса калькулятора для расчета скорости инфузии " +
        "препарата через линеомат (скорость титрования)")
public class TitrationCalculatorRequest extends BaseCalculatorRequest {
    @Schema(description = "Вес человека в кг", example = "65")
    private Double weightPatient;
    @Schema(description = "Дозировка препарата в мкг*кг/мин или мл/час", example = "2")
    private Double dosage;
    @Schema(description = "Количество препарата в мг", example = "10")
    private Double amountOfDrug;
    @Schema(description = "Общий объем раствора в мл", example = "50")
    private Double volumeOfSolution;
    @Schema(description = "Дозировка в мл/час?", example = "true")
    private Boolean isMlInHour;
}
