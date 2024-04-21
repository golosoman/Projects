package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import com.example.MedicalCalculators.dto.response.CalculatorInfo;
import com.example.MedicalCalculators.dto.response.CalculatorInfoFull;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public abstract class BaseCalculator<BaseCalculatorRequest> implements ICalculator<BaseCalculatorRequest>{
    private final CalculatorType type;
    private final String description;

    @Override
    public CalculatorInfo getInfo(){
        return new CalculatorInfo(getDescription());
    };
    @Override
    public CalculatorInfoFull getInfoFull(){
        return new CalculatorInfoFull((long) type.getId(), type.getName(), getDescription());
    };

    @Override
    public abstract CalculatorResult calculate(BaseCalculatorRequest request);

}
