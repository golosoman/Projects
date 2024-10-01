package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.response.CalculatorInfo;
import com.example.MedicalCalculators.dto.response.CalculatorInfoFull;
import com.example.MedicalCalculators.dto.response.CalculatorResult;

public interface ICalculator<BaseCalculatorRequest> {
    CalculatorInfo getInfo();

    CalculatorInfoFull getInfoFull();

    CalculatorResult calculate(BaseCalculatorRequest request);
}
