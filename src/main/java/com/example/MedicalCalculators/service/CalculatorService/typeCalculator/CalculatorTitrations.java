package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import lombok.extern.log4j.Log4j2;

import java.text.DecimalFormat;

@Log4j2
public class CalculatorTitrations extends BaseCalculator<TitrationCalculatorRequest> {

    public CalculatorTitrations() {
        super(CalculatorType.TITRATIONS, "*Расчет скорости внутривенного капельного введения препарата\nФормула: количество капель в " +
                "минуту = V*20/t, где V - объем раствора в милилитрах, t - время в минутах, 20 - среднее " +
                "количество капель в милилитре, v - скорость введения в каплях в минуту");
        log.info("CalculatorRateIntravenousDripDrug has been created");
    }

    // Расчет скорости инфузии препарата через линеомат (скорость титрования),
    // результат в мл/час
    public CalculatorResult calculate(TitrationCalculatorRequest calculatorRequest) {
        double infusionRate = calculatorRequest.getWeightPatient() * calculatorRequest.getDosage() /
                (calculatorRequest.getAmountOfDrug() * (1000 /
                        calculatorRequest.getVolumeOfSolution())) * 60;
        log.debug("The result was obtained using a BMI calculator: " + infusionRate);
        return new CalculatorResult((new DecimalFormat("#.###")).format(infusionRate));
    }
}
