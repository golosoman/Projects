package com.example.MedicalCalculators.dto.request.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.BaseCalculatorRequest;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class TitrationCalculatorRequest extends BaseCalculatorRequest {
    // Вес пациента, кг
    private Double weightPatient;
    // Дозировка в мкг*кг/мин или мл/час
    private Double dosage;
    // Количество препарата, мг
    private Double amountOfDrug;
    // Общий объем раствора, мл
    private Double volumeOfSolution;
}
