package com.example.MedicalCalculators.dto.request.typeCalculator;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.validator.constraints.Range;

@Setter
@Getter
@AllArgsConstructor
@Schema(description = "Объект, включающий параметры для калькулятора расчета скорости инфузии " +
        "препарата через линеомат (скорость титрования)")
public class TitrationCalculatorRequest extends BaseCalculatorRequest {
    @Schema(description = "Вес человека в кг", example = "65")
    @Range(min = 10, max = 800, message = "'Вес' не должен быть меньше 10 кг и не должен превышать 800 кг")
    @NotNull(message = "Параметр 'вес' человека обязательный для заполнения")
    private Double weightPatient;

    @Schema(description = "Дозировка препарата в мкг*кг/мин или мл/час", example = "2")
    @Positive(message = "'Дозировка препарата' строго положительная")
    @DecimalMin(value = "0.1", message = "Значение параметра 'дозировка препарата' должно " +
            "быть не меньше 0.1 мкг*кг/мин или мл/час")
    @NotNull(message = "Параметр 'дозировка препарата' обязательный для заполнения")
    private Double dosage;

    @Schema(description = "Количество препарата в мг", example = "10")
    @Positive(message = "Значение 'количества препарата' является строго положительным")
    @Min(value = 1, message = "Минимальное значение 'количества препарата' составляет 1 мг")
    @NotNull(message = "Параметр 'количество препарата' обязательный для заполнения")
    private Double amountOfDrug;

    @Schema(description = "Общий объем раствора в мл", example = "50")
    @Positive(message = "Значение 'общего объема раствора' является строго положительным")
    @Min(value = 1, message = "Минимальное значение 'общего объема раствора' составляет 1 мл")
    @NotNull(message = "Параметр 'общий объем раствора' обязательный для заполнения")
    private Double volumeOfSolution;

    @Schema(description = "Дозировка в мл/час?", example = "true")
    @NotNull(message = "Параметр 'дозировка в мл/час?' обязательный для заполнения")
    private Boolean isMlInHour;
}
