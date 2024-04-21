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
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class CalculatorService {
    private final Map<CalculatorType, BaseCalculator> calculators = new HashMap<>();

    public CalculatorService() {
        calculators.put(CalculatorType.BODY_MASS_INDEX, new CalculatorBodyMassIndex());
        calculators.put(CalculatorType.RATE_INTRAVENOUS_DRIP_DRUG, new CalculatorRateIntravenousDripDrug());
        calculators.put(CalculatorType.TITRATIONS, new CalculatorTitrations());
    }

    private CalculatorInfoFull findCalculatorById(Long id) {
        for (Map.Entry<CalculatorType, BaseCalculator> entry : calculators.entrySet()) {
            if (entry.getKey().getId() == id) {
                return entry.getValue().getInfoFull();
            }
        }
        throw new NotFoundException("Calculator with ID " + id + " not found");
    }

    private CalculatorInfo findCalculatorByName(String name) {
        for (Map.Entry<CalculatorType, BaseCalculator> entry : calculators.entrySet()) {
            if (Objects.equals(entry.getKey().getName(), name)) {
                return entry.getValue().getInfo();
            }
        }
        throw new NotFoundException("Calculator with name " + name + " not found");
    }

    public CalculatorInfoFull getOne(Long id) {
        CalculatorInfoFull calculatorInfoFull = findCalculatorById(id);
        if (calculatorInfoFull == null) {
            throw new NotFoundException("Calculator with ID " + id + " not found");
        }
        return calculatorInfoFull;
    }

    public List<CalculatorInfoFull> getAll() {
        List<CalculatorInfoFull> calculatorsInfo = new ArrayList<>();
        for (Map.Entry<CalculatorType, BaseCalculator> entry : calculators.entrySet()) {
            calculatorsInfo.add(entry.getValue().getInfoFull());
        }
        return calculatorsInfo;
    }

    public CalculatorInfo getInfo(String name) {
        CalculatorInfo calculatorInfoFull = findCalculatorByName(name);
        if (calculatorInfoFull == null) {
            throw new NotFoundException("Calculator with name " + name + " not found");
        }
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