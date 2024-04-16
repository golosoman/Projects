package com.example.MedicalCalculators.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class RIDDCalculatorRequest {
    // Объем раствора, мл
    private Double volumeOfSolution;
    // Желаемое время введения, минут
    private Double timeTaking;
}
