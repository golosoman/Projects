package com.example.MedicalCalculators.service.CalculatorService;

import com.example.MedicalCalculators.dto.request.typeCalculator.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.BaseCalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.RIDDCalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorInfoFull;
import com.example.MedicalCalculators.dto.response.CalculatorInfo;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.exceptions.NotFoundException;
import com.example.MedicalCalculators.service.CalculatorService.typeCalculator.*;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
@Log4j2
public class CalculatorService {
    private final Map<CalculatorType, BaseCalculator> calculators = new HashMap<>();

    public CalculatorService() {
        calculators.put(CalculatorType.BODY_MASS_INDEX, new CalculatorBodyMassIndex());
        calculators.put(CalculatorType.RATE_INTRAVENOUS_DRIP_DRUG, new CalculatorRateIntravenousDripDrug());
        calculators.put(CalculatorType.TITRATIONS, new CalculatorTitrations());
        log.info("CalculatorService has been created");
    }

    private CalculatorInfoFull findCalculatorById(Long id) {
        for (Map.Entry<CalculatorType, BaseCalculator> entry : calculators.entrySet()) {
            if (entry.getKey().getId() == id) {
                log.debug("The calculator was found using the method: findCalculatorById");
                return entry.getValue().getInfoFull();
            }
        }
        log.warn("Exception will be thrown on method: findCalculatorById");
        throw new NotFoundException("Calculator with ID " + id + " not found");
    }

    private CalculatorInfo findCalculatorByName(String name) {
        for (Map.Entry<CalculatorType, BaseCalculator> entry : calculators.entrySet()) {
            if (Objects.equals(entry.getKey().getName(), name)) {
                log.debug("The calculator was found using the method: findCalculatorByName");
                return entry.getValue().getInfo();
            }
        }
        log.warn("Exception will be thrown on method: findCalculatorByName");
        throw new NotFoundException("Calculator with name " + name + " not found");
    }

    public CalculatorInfoFull getOne(Long id) {
        CalculatorInfoFull calculatorInfoFull = findCalculatorById(id);
        if (calculatorInfoFull == null) {
            log.warn("Exception will be thrown on method: getOne");
            throw new NotFoundException("Calculator with ID " + id + " not found");
        }
        log.debug("The calculator was found using the method: getOne");
        return calculatorInfoFull;
    }

    public List<CalculatorInfoFull> getAll() {
        List<CalculatorInfoFull> calculatorsInfo = new ArrayList<>();
        for (Map.Entry<CalculatorType, BaseCalculator> entry : calculators.entrySet()) {
            log.debug("There is at least one calculator in calculators");
            calculatorsInfo.add(entry.getValue().getInfoFull());
        }
        log.debug("Information about calculators has been returned");
        return calculatorsInfo;
    }

    public CalculatorInfo getInfo(String name) {
        CalculatorInfo calculatorInfoFull = findCalculatorByName(name);
        if (calculatorInfoFull == null) {
            log.warn("Exception will be thrown on method: getInfo");
            throw new NotFoundException("Calculator with name " + name + " not found");
        }
        log.debug("The calculator was found using the method: getInfo");
        return calculatorInfoFull;

    }

    public CalculatorResult getBMIResult(BMICalculatorRequest calculatorRequest) {
        log.debug("Start method getBMIResult");
        return calculators.get(CalculatorType.BODY_MASS_INDEX).calculate(calculatorRequest);
    }

    public CalculatorResult getTitrationResult(TitrationCalculatorRequest calculatorRequest) {
        log.debug("Start method getTitrationResult");
        return calculators.get(CalculatorType.TITRATIONS).calculate(calculatorRequest);
    }

    public CalculatorResult getRIDDResult(RIDDCalculatorRequest calculatorRequest) {
        log.debug("Start method getRIDDResult");
        return calculators.get(CalculatorType.RATE_INTRAVENOUS_DRIP_DRUG).calculate(calculatorRequest);
    }
}