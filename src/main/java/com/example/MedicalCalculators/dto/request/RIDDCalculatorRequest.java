package com.example.MedicalCalculators.dto.request;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class RIDDCalculatorRequest {
    // Объем раствора, мл
    private Double volumeOfSolution;
    // Желаемое время введения, минут
    private Double timeTaking;
}
