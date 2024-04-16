package com.example.MedicalCalculators.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;


@Data
@AllArgsConstructor
public class TitrationCalculatorRequest {
    // Вес пациента, кг
    private Double weightPatient;
    // Дозировка в мкг*кг/мин или мл/час
    private Double dosage;
    // Количество препарата, мг
    private Double amountOfDrug;
    // Общий объем раствора, мл
    private Double volumeOfSolution;
}