package com.example.MedicalCalculators.service.CalculatorService;

//import com.example.MedicalCalculators.entity.CalculatorEntity;

import com.example.MedicalCalculators.dto.request.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.request.RIDDCalculatorRequest;
import com.example.MedicalCalculators.dto.request.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorID;
import com.example.MedicalCalculators.dto.response.CalculatorInfoFull;
import com.example.MedicalCalculators.dto.response.CalculatorInfo;
import com.example.MedicalCalculators.dto.request.CalculatorInfoRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.exceptions.AlreadyExistsException;
import com.example.MedicalCalculators.exceptions.NotFoundException;
//import com.example.MedicalCalculators.repository.CalculatorRepository;
import com.example.MedicalCalculators.service.CalculatorService.typeCalculator.CalculatorBodyMassIndex;
import com.example.MedicalCalculators.service.CalculatorService.typeCalculator.CalculatorRateIntravenousDripDrug;
import com.example.MedicalCalculators.service.CalculatorService.typeCalculator.CalculatorTitrations;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class CalculatorService {
    private static final List<CalculatorInfoFull> CALCULATOR_LIST = new ArrayList<>();

    static {
        CALCULATOR_LIST.add(new CalculatorInfoFull(1L, "BodyMassIndex",
                "*Этот калькулятор позволяет быстро и просто рассчитать индекс массы тела(ИМТ)." +
                        "\nФормула: I=m/h^2 где: m — масса тела в килограммах; h — рост в метрах; измеряется в " +
                        "кг/м².\nКалькулятор рачитывает показатели в следующих интервалах: рост не более 300 см; " +
                        "вес не менее 10 кг.\nВозможен ввод дробных значений веса с точность до одного знака " +
                        "после запятой."));
        CALCULATOR_LIST.add(new CalculatorInfoFull(2L, "RateIntravenousDripDrug",
                "*Этот калькулятор позволяет расчитать скорость инфузии препарата через линеомат " +
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
                        "(1 000/общий объем инфузионного раствора))*60"));
        CALCULATOR_LIST.add(new CalculatorInfoFull(3L, "Titrations",
                "*Расчет скорости внутривенного капельного введения препарата\nФормула: количество капель в " +
                        "минуту = V*20/t, где V - объем раствора в милилитрах, t - время в минутах, 20 - среднее " +
                        "количество капель в милилитре, v - скорость введения в каплях в минуту"));
    }

    private static CalculatorInfoFull findCalculatorByName(String name) {
        for (CalculatorInfoFull calculatorInfoFull : CALCULATOR_LIST) {
            if (calculatorInfoFull.getName().equals(name)) {
                return calculatorInfoFull;
            }
        }
        return null;
    }

    private static CalculatorInfoFull findCalculatorById(Long id) {
        for (CalculatorInfoFull calculatorInfoFull : CALCULATOR_LIST) {
            if (calculatorInfoFull.getId().equals(id)) {
                return calculatorInfoFull;
            }
        }
        return null;
    }

    public static Long getLastIdInList() {
        if (CALCULATOR_LIST.isEmpty()) {
            return 0L;
        }
        CalculatorInfoFull lastCalculatorInfoFull = CALCULATOR_LIST.get(CALCULATOR_LIST.size() - 1);
        return lastCalculatorInfoFull.getId();
    }

    public CalculatorInfoFull getOne(Long id) {
        CalculatorInfoFull calculatorInfoFull = findCalculatorById(id);
        if (calculatorInfoFull == null) {
            throw new NotFoundException("Calculator with ID " + id + " not found");
        }
        return calculatorInfoFull;
    }

    public CalculatorInfoFull add(CalculatorInfoRequest calculatorInfoRequest) {
        if (findCalculatorByName(calculatorInfoRequest.getName()) != null) {
            throw new AlreadyExistsException("Calculator with name "
                    + calculatorInfoRequest.getName()
                    + " alreadyExists");
        }
        CalculatorInfoFull calculatorInfoFull = new CalculatorInfoFull(
                getLastIdInList() + 1,
                calculatorInfoRequest.getName(),
                calculatorInfoRequest.getDescription());
        CALCULATOR_LIST.add(calculatorInfoFull);
        return calculatorInfoFull;
    }

    public List<CalculatorInfoFull> getAll() {
        return CALCULATOR_LIST;
    }

    public CalculatorInfo getInfo(String name) {
        CalculatorInfoFull calculatorInfoFull = findCalculatorByName(name);
        if (calculatorInfoFull == null) {
            throw new NotFoundException("Calculator with name " + name + " not found");
        }
        return new CalculatorInfo(calculatorInfoFull.getDescription());

    }

    public CalculatorInfoFull delete(Long id) {
        Iterator<CalculatorInfoFull> iterator = CALCULATOR_LIST.iterator();
        while (iterator.hasNext()) {
            CalculatorInfoFull calculatorInfoFull = iterator.next();
            if (calculatorInfoFull.getId().equals(id)) {
                iterator.remove(); // Удаляем элемент, если его Id совпадает с заданным
                return calculatorInfoFull;
            }
        }
        throw new NotFoundException("Calculator with ID " + id + " not found");
    }

    public CalculatorInfoFull update(Long id, CalculatorInfoRequest calculatorInfoRequest) {
        CalculatorInfoFull calculatorInfoFull = findCalculatorById(id);
        if (calculatorInfoFull == null) {
            throw new NotFoundException("Calculator with ID " + id + " not found");
        }
        calculatorInfoFull.setName(calculatorInfoRequest.getName());
        calculatorInfoFull.setDescription(calculatorInfoRequest.getDescription());
        return calculatorInfoFull;
    }

    public CalculatorResult getBMIResult(BMICalculatorRequest calculatorRequest) {
        return new CalculatorBodyMassIndex().calculate(calculatorRequest);
    }

    public CalculatorResult getTitrationResult(TitrationCalculatorRequest calculatorRequest) {
        return new CalculatorTitrations().calculate(calculatorRequest);
    }

    public CalculatorResult getRIDDResult(RIDDCalculatorRequest calculatorRequest) {
        return new CalculatorRateIntravenousDripDrug().calculate(calculatorRequest);
    }

}