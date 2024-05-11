package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.RIDDCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import lombok.extern.log4j.Log4j2;

import java.text.DecimalFormat;

@Log4j2
public class CalculatorRateIntravenousDripDrug extends BaseCalculator<RIDDCalculatorRequest> {
    public CalculatorRateIntravenousDripDrug() {
        super(CalculatorType.RATE_INTRAVENOUS_DRIP_DRUG,
                """
                        *Расчет скорости внутривенного капельного введения препарата\nФормула: 
                        количество капель в минуту = V*20/t, где V - объем раствора в милилитрах, 
                        t - время в минутах, 20 - среднее количество капель в милилитре, 
                        v - скорость введения в каплях в минуту
                        """);
        log.info("Создан калькулятор скорости внутривенного капельного введения препарата");
    }

    // Расчет скорости внутривенного капельного введения препарата, результат в каплях в минуту
    public CalculatorResult calculate(RIDDCalculatorRequest calculatorRequest) {
        double time = calculatorRequest.getTimeTaking();
        if (!calculatorRequest.getIsMinute()) {
            time *= 60;
        }
        double ridd = calculatorRequest.getVolumeOfSolution() * 20 / time;
        log.debug("Результат был получен с помощью калькулятора внутривенного введения препарата: " + ridd);
        return new CalculatorResult((new DecimalFormat("#.###")).format(ridd));
    }
}
