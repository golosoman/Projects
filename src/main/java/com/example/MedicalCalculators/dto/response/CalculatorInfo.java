package com.example.MedicalCalculators.dto.response;

import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
@Schema(description = "Объект информации о калькуляторе")
public class CalculatorInfo {
    @Schema(description = "Информация о калькуляторе", example = "Этот калькулятор позволяет быстро и " +
            "просто рассчитать индекс массы тела(ИМТ).")
    private String info;
}
