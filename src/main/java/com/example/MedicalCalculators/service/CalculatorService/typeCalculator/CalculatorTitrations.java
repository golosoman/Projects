package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.exceptions.ParameterException;
import com.example.MedicalCalculators.model.result.Result;

import java.text.DecimalFormat;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class CalculatorTitrations implements ICalculator {
    private final Set<String> key = new HashSet<>(Set.of("weightPatient", "dosage",
            "amountOfDrug", "volumeOfSolution"));

    @Override
    public Result calculate(Map<String, String> parameters) throws ParameterException {
        if (!key.equals(parameters.keySet())) {
            throw new ParameterException("Неверно указаны параметры!");
        }
        double infusionRate;
        try {
            infusionRate = Double.parseDouble(parameters.get("weightPatient")) *
                    Double.parseDouble(parameters.get("dosage")) /
                    (Double.parseDouble(parameters.get("amountOfDrug")) *
                            (1000 / Double.parseDouble(parameters.get("volumeOfSolution"))))*60;
        } catch (Exception e) {
            throw new ParameterException("Неверно указаны параметры!");
        }
        return Result.toModel((new DecimalFormat("#.###")).format(infusionRate));
    }
}
