package com.example.MedicalCalculators.model.calculator;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

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

    public static List<Calculator> toModelList(Iterable<CalculatorEntity> entities) {
        List<Calculator> list = new ArrayList<Calculator>();
        entities.forEach((entity) -> {
            Calculator model = Calculator.toModel(entity);
            list.add(model);
        });
        return list;
    }
}
