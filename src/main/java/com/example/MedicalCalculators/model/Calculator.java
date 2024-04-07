package com.example.MedicalCalculators.model;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class Calculator {
    private Long id;
    private String name;
    private String description;
    private String formula;

    public static Calculator toModel(CalculatorEntity entity) {
        Calculator model = new Calculator();
        model.setId(entity.getId());
        model.setName(entity.getName());
        model.setDescription(entity.getDescription());
        model.setFormula(entity.getFormula());
        return model;
    }

//    public static List<Calculator> toModel(Iterable<CalculatorEntity> entities)
}
