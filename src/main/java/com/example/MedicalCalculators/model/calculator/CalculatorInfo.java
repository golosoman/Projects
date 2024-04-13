package com.example.MedicalCalculators.model.calculator;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class CalculatorInfo {
    private String info;
    public static CalculatorInfo toModel(CalculatorEntity entity) {
        CalculatorInfo model = new CalculatorInfo();
        model.setInfo(entity.getDescription());
        return model;
    }
}
