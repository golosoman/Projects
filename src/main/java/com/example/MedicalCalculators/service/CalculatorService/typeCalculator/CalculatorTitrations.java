package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.request.typeCalculator.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import lombok.extern.log4j.Log4j2;

import java.text.DecimalFormat;

@Log4j2
public class CalculatorTitrations extends BaseCalculator<TitrationCalculatorRequest> {

    public CalculatorTitrations() {
        super(CalculatorType.TITRATIONS, "*Этот калькулятор позволяет " +
                "расчитать скорость инфузии препарата через линеомат " +
                "(скорость титрования в мл/час) при известном количестве препарата в милиграммах в известном " +
                "объеме раствора. Также необходимо указать вес пациента и дозировку, определяемую либо в " +
                "мкг*кг/мин, либо в мл/час.\nСкорость в мл/час автоматически пересчитывается в скорость " +
                "в каплях в минуту при указании дозировки препарата в микрограммах на килограмм в " +
                "минуту. При этом в рачет берется то, что в 1 милилитр содержит 20 капель.\nЕсли " +
                "скорость в каплях в минуту менее 1 капли в минуту, калькулятор предлагает " +
                "выбрать меньшее разведение и перейти с капельного введения на введение с помощью " +
                "линеомата.\nТакже калькулятор позволяет рассчитать скорость инфузии в мкг*кг/мин при " +
                "известной дозировке препарата в мл/час.\nДля того, чтобы использовать калькулятор при " +
                "расчете доз препаратов, не зависящих от веса, в поле \"Вес пациента\" введите значение " +
                "равное 1.\nФормула: Скорость инфузии = масса тела пациента (кг) * доза препарата " +
                "(мкг/кг*мин) / (количество препарата в инфузионном растворе (мг) * " +
                "(1 000/общий объем инфузионного раствора))*60");
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
