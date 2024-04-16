package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.request.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.exceptions.ParameterException;
import org.springframework.stereotype.Component;

import java.text.DecimalFormat;


@Component
public class CalculatorBodyMassIndex {
    // Расчет индекса массы тела, результат в кг/м^2
    public CalculatorResult calculate(BMICalculatorRequest calculatorRequest) {
        if (calculatorRequest.getHeight() <= 0 | calculatorRequest.getHeight() > 300){
            throw new ParameterException("Incorrect value for height");
        }

        if (calculatorRequest.getWeightPatient() < 10){
            throw new ParameterException("Incorrect value for weight");
        }
        double bmi = calculatorRequest.getWeightPatient() /
                Math.pow(calculatorRequest.getHeight() / 100, 2);
        return new CalculatorResult((new DecimalFormat("#.###")).format(bmi));
    }
}
