package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import lombok.extern.log4j.Log4j2;

import java.text.DecimalFormat;

@Log4j2
public class CalculatorBodyMassIndex extends BaseCalculator<BMICalculatorRequest> {
    public CalculatorBodyMassIndex() {
        super(CalculatorType.BODY_MASS_INDEX, "*Этот калькулятор позволяет " +
                "быстро и просто рассчитать индекс массы тела(ИМТ)." +
                "\nФормула: I=m/h^2 где: m — масса тела в килограммах; h — рост в метрах; измеряется в " +
                "кг/м².\nКалькулятор рачитывает показатели в следующих интервалах: рост не более 300 см; " +
                "вес не менее 10 кг.\nВозможен ввод дробных значений веса с точность до одного знака " +
                "после запятой.");
        log.info("CalculatorBodyMassIndex has been created");
    }

    // Расчет индекса массы тела, результат в кг/м²
    @Override
    public CalculatorResult calculate(BMICalculatorRequest calculatorRequest) {
        double bmi = calculatorRequest.getWeightPatient() /
                Math.pow(calculatorRequest.getHeight() / 100, 2);
        log.debug("The result was obtained using a BMI calculator: " + bmi);
        return new CalculatorResult((new DecimalFormat("#.###")).format(bmi));
    }
}
