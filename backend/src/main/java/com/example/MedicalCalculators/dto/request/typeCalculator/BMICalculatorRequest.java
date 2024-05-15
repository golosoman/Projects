package com.example.MedicalCalculators.dto.request.typeCalculator;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.validator.constraints.Range;

@Setter
@Getter
@AllArgsConstructor
@Schema(description = "Объект, включающий параметры для калькулятора индекса массы тела")
public class BMICalculatorRequest extends BaseCalculatorRequest {
    @Schema(description = "Вес человека в кг", example = "65")
    @Range(min = 10, max = 800, message = "'Вес' не должен быть меньше 10 кг и не должен превышать 800 кг")
    @NotNull(message = "Параметр 'вес' пациента является обязательным")
    private Double weightPatient;

    @Schema(description = "Рост человека в см", example = "176")
    @Range(min = 45, max = 300, message = "'Рост' должен быть меньше 45 см и не должен превышать 300 см")
    @NotNull(message = "Параметр 'рост' пациента является обязательным")
    private Double height;
}
