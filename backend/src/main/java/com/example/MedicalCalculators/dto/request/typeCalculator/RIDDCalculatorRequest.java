package com.example.MedicalCalculators.dto.request.typeCalculator;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
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
    @Positive(message = "Значение 'объема раствора' строго положительное")
    @Min(value = 1, message = "Минимальное значение 'объема раствора' 1 мл")
    @NotNull(message = "Параметр 'объем раствора' обязательный для заполнения")
    private Double volumeOfSolution;

    @Schema(description = "Желаемое время введения препарата в минутах/часах", example = "30")
    @Positive(message = "Значение 'желаемого времени введения препарата' является строго положительным")
    @DecimalMin(value = "0.1", message = "Значение параметра 'желаемое время введения препарата' должно " +
            "быть не меньше 0.1 минуты/часа")
    @NotNull(message = "Параметр 'желаемое время введения препарата' обязательный для заполнения")
    private Double timeTaking;

    @Schema(description = "Время в минутах?", example = "true")
    @NotNull(message = "Параметр 'время в минутах?' обязательный для заполнения")
    private Boolean isMinute;
}
