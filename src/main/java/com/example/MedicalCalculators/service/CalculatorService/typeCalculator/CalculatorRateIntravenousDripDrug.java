package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.request.RIDDCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.exceptions.ParameterException;
import lombok.Getter;
import lombok.Setter;
import org.springframework.stereotype.Component;

import java.text.DecimalFormat;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

@Component
public class CalculatorRateIntravenousDripDrug {
    // Расчет скорости внутривенного капельного введения препарата, результат в каплях в минуту
    public CalculatorResult calculate(RIDDCalculatorRequest calculatorRequest) throws ParameterException {
//        if (calculatorRequest.getVolumeOfSolution() <= 0){
//            throw new ParameterException("Incorrect value for VolumeOfSolution");
//        }
//        if (calculatorRequest.getTimeTaking() <= 0){
//            throw new ParameterException("Incorrect value for TimeTaking");
//        }
        double ridd = calculatorRequest.getVolumeOfSolution() * 20 /
                calculatorRequest.getTimeTaking();
        return new CalculatorResult((new DecimalFormat("#.###")).format(ridd));
    }
}
