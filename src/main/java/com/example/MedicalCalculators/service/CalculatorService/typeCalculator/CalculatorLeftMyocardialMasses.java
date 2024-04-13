package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.entity.ParameterEntity;
import com.example.MedicalCalculators.exceptions.ParameterException;
import com.example.MedicalCalculators.model.result.Result;
import lombok.Getter;
import lombok.Setter;
import org.springframework.stereotype.Component;

import java.text.DecimalFormat;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

@Component
@Getter
@Setter
public class CalculatorLeftMyocardialMasses implements ICalculator {
    private Set<String> key;
    public CalculatorLeftMyocardialMasses(Set<ParameterEntity> parameterKeys){
        key = parameterKeys.stream().map(ParameterEntity::getName).collect(Collectors.toSet());
    }
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
}}
