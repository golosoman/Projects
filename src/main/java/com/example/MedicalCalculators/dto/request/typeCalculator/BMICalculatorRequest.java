package com.example.MedicalCalculators.dto.request.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.BaseCalculatorRequest;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class BMICalculatorRequest extends BaseCalculatorRequest {
    // Вес, кг
    private Double weightPatient;
    // Рост, см
    private Double height;
}
