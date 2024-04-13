package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.exceptions.ParameterException;
import com.example.MedicalCalculators.model.result.Result;

import java.util.Map;

public interface ICalculator {

    Result calculate(Map<String, String> parameters) throws ParameterException;
}
