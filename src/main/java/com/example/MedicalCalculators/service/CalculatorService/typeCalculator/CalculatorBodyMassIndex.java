package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.request.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
//import com.example.MedicalCalculators.model.result.Result;
import org.springframework.stereotype.Component;

import java.text.DecimalFormat;


@Component
public class CalculatorBodyMassIndex{
    // Расчет индекса массы тела, результат в кг/м^2
    public CalculatorResult calculate(BMICalculatorRequest calculatorRequest){
        double bmi = calculatorRequest.getWeightPatient() /
                    Math.pow(calculatorRequest.getHeight() / 100, 2);
        return new CalculatorResult((new DecimalFormat("#.###")).format(bmi));
    }
}
