package com.example.MedicalCalculators.service.CalculatorService;

import com.example.MedicalCalculators.dto.request.typeCalculator.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.RIDDCalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorInfoFull;
import com.example.MedicalCalculators.dto.response.CalculatorInfo;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.exceptions.api.NotFoundException;
import com.example.MedicalCalculators.service.CalculatorService.typeCalculator.*;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;

import java.util.*;

@Log4j2
@Service
@Validated
public class CalculatorService {
    private final Map<CalculatorType, BaseCalculator> calculators = new HashMap<>();

    public CalculatorService() {
        calculators.put(CalculatorType.BODY_MASS_INDEX, new CalculatorBodyMassIndex());
        calculators.put(CalculatorType.RATE_INTRAVENOUS_DRIP_DRUG, new CalculatorRateIntravenousDripDrug());
        calculators.put(CalculatorType.TITRATIONS, new CalculatorTitrations());
        log.info("Создан сервис калькулятора");
    }

    private CalculatorInfoFull findCalculatorById(Long id) {
        for (Map.Entry<CalculatorType, BaseCalculator> entry : calculators.entrySet()) {
            if (entry.getKey().getId() == id) {
                log.debug("Калькулятор был найден с помощью метода: findCalculatorById");
                return entry.getValue().getInfoFull();
            }
        }
        log.warn("Для метода: findCalculatorById будет выдано исключение");
        throw new NotFoundException("Калькулятор с идентификатором " + id + " не был найден");
    }

    private CalculatorInfo findCalculatorByName(String name) {
        for (Map.Entry<CalculatorType, BaseCalculator> entry : calculators.entrySet()) {
            if (Objects.equals(entry.getKey().getName(), name)) {
                log.debug("Калькулятор был найден с помощью метода: findCalculatorByName");
                return entry.getValue().getInfo();
            }
        }
        log.warn("Для метода: findCalculatorByName будет выдано исключени");
        throw new NotFoundException("Калькулятор с названием " + name + " не был найден");
    }

    public CalculatorInfoFull getOne(@Min(value = 0, message = "Идентификатор должен быть не меньше 0") Long id) {
        CalculatorInfoFull calculatorInfoFull = findCalculatorById(id);
        if (calculatorInfoFull == null) {
            log.warn("Для метода: getOne будет выдано исключение");
            throw new NotFoundException("Калькулятор с идентификатором " + id + " не был найден");
        }
        log.debug("Калькулятор был найден с помощью метода: getOne");
        return calculatorInfoFull;
    }

    public List<CalculatorInfoFull> getAll() {
        List<CalculatorInfoFull> calculatorsInfo = new ArrayList<>();
        for (Map.Entry<CalculatorType, BaseCalculator> entry : calculators.entrySet()) {
            log.debug("В калькуляторах есть по крайней мере один калькулятор");
            calculatorsInfo.add(entry.getValue().getInfoFull());
        }
        log.debug("Информация о калькуляторах была возвращена");
        return calculatorsInfo;
    }

    public CalculatorInfo getInfo(@NotBlank(message = "Имя калькулятора не может быть пустым") String name) {
        CalculatorInfo calculatorInfoFull = findCalculatorByName(name);
        if (calculatorInfoFull == null) {
            log.warn("Для метода: getInfo будет выдано исключение");
            throw new NotFoundException("Калькулятор с названием " + name + " не был найден");
        }
        log.debug("Калькулятор был найден с помощью метода: getInfo");
        return calculatorInfoFull;

    }

    public CalculatorResult getBMIResult(@Valid BMICalculatorRequest calculatorRequest) {
        log.debug("Запущен метод getBMIResult");
        return calculators.get(CalculatorType.BODY_MASS_INDEX).calculate(calculatorRequest);
    }

    public CalculatorResult getTitrationResult(@Valid TitrationCalculatorRequest calculatorRequest) {
        log.debug("Запущен метод getTitrationResult");
        return calculators.get(CalculatorType.TITRATIONS).calculate(calculatorRequest);
    }

    public CalculatorResult getRIDDResult(@Valid RIDDCalculatorRequest calculatorRequest) {
        log.debug("Запущен метод getRIDDResult");
        return calculators.get(CalculatorType.RATE_INTRAVENOUS_DRIP_DRUG).calculate(calculatorRequest);
    }
}