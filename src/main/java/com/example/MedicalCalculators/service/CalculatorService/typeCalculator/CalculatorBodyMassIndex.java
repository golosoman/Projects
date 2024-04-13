package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.exceptions.ParameterException;
import com.example.MedicalCalculators.model.result.Result;
import lombok.Getter;
import lombok.Setter;
import org.springframework.stereotype.Component;

import java.text.DecimalFormat;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

@Component
@Getter
@Setter
public class CalculatorBodyMassIndex implements ICalculator{
    private final Set<String> key = new HashSet<>(Set.of("weightPatient", "height"));
    @Override
    public Result calculate(Map<String, String> parameters) throws ParameterException {
        if (!key.equals(parameters.keySet())) {
            throw new ParameterException("Неверно указаны параметры!");
        }
        double infusionRate;
        try {
            infusionRate = Double.parseDouble(parameters.get("weightPatient")) /
                    Math.pow(Double.parseDouble(parameters.get("height"))/100, 2);
        } catch (Exception e) {
            throw new ParameterException("Неверно указаны параметры!");
        }
        return Result.toModel((new DecimalFormat("#.###")).format(infusionRate));
    }
}
