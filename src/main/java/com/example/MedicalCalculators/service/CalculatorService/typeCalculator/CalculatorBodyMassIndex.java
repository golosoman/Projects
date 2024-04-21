package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.exceptions.ParameterException;
import org.springframework.stereotype.Component;

import java.text.DecimalFormat;

public class CalculatorBodyMassIndex extends BaseCalculator<BMICalculatorRequest> {
    public CalculatorBodyMassIndex() {
        super(CalculatorType.BODY_MASS_INDEX, "*Этот калькулятор позволяет " +
                "быстро и просто рассчитать индекс массы тела(ИМТ)." +
                "\nФормула: I=m/h^2 где: m — масса тела в килограммах; h — рост в метрах; измеряется в " +
                "кг/м².\nКалькулятор рачитывает показатели в следующих интервалах: рост не более 300 см; " +
                "вес не менее 10 кг.\nВозможен ввод дробных значений веса с точность до одного знака " +
                "после запятой.");
    }

    @Override
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
