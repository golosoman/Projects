package com.example.MedicalCalculators.dto.response;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Schema(description = "Объект полной ифнормации о калькуляторе", contentMediaType = "application/json")
public class CalculatorInfoFull extends CalculatorInfo {
    @Schema(description = "Идентификатор", example = "1")
    private Long id;
    @Schema(description = "Название калькулятора", example = "Body Mass Index")
    private String name;

    public CalculatorInfoFull(Long id, String name, String info) {
        super(info);
        this.id = id;
        this.name = name;
    }
}
