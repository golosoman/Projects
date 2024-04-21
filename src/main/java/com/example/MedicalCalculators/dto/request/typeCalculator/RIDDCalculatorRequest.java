package com.example.MedicalCalculators.dto.request.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.BaseCalculatorRequest;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class RIDDCalculatorRequest extends BaseCalculatorRequest {
    // Объем раствора, мл
    private Double volumeOfSolution;
    // Желаемое время введения, минут
    private Double timeTaking;
}
