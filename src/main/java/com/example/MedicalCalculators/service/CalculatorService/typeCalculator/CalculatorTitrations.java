package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.request.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.exceptions.ParameterException;
import org.springframework.stereotype.Component;
//import com.example.MedicalCalculators.model.result.Result;

import java.text.DecimalFormat;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;


@Component
public class CalculatorTitrations{
    // Расчет скорости инфузии препарата через линеомат (скорость титрования),
    // результат в мл/час
    public CalculatorResult calculate(TitrationCalculatorRequest calculatorRequest){
        double infusionRate = calculatorRequest.getWeightPatient() * calculatorRequest.getDosage() /
                (calculatorRequest.getAmountOfDrug() *  (1000 /
                calculatorRequest.getVolumeOfSolution())) * 60;
        return new CalculatorResult((new DecimalFormat("#.###")).format(infusionRate));
    }
}
