package com.example.MedicalCalculators.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class BMICalculatorRequest {
    // Вес, кг
    private Double weightPatient;
    // Рост, см
    private Double height;
}
