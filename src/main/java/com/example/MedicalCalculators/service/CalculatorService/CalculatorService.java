package com.example.MedicalCalculators.service.CalculatorService;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import com.example.MedicalCalculators.exceptions.AlreadyExistsException;
import com.example.MedicalCalculators.exceptions.NotFoundException;
import com.example.MedicalCalculators.exceptions.ParameterException;
import com.example.MedicalCalculators.model.calculator.Calculator;
import com.example.MedicalCalculators.model.calculator.CalculatorInfo;
import com.example.MedicalCalculators.service.CalculatorService.typeCalculator.CalculatorBodyMassIndex;
import com.example.MedicalCalculators.service.CalculatorService.typeCalculator.CalculatorRateIntravenousDripDrug;
import com.example.MedicalCalculators.service.CalculatorService.typeCalculator.CalculatorTitrations;
import com.example.MedicalCalculators.model.result.Result;
import com.example.MedicalCalculators.repository.CalculatorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class CalculatorService {
    @Autowired
    private CalculatorRepository calculatorRepository;

    public CalculatorEntity add(CalculatorEntity calculator) throws AlreadyExistsException {
        if (calculatorRepository.findByName(calculator.getName()) != null) {
            throw new AlreadyExistsException("Калькулятор с таким именем уже существует");
        }
        return calculatorRepository.save(calculator);
    }

    public Calculator getOne(Long id) throws NotFoundException {
        CalculatorEntity calculator = calculatorRepository.findById(id).get();
        if (calculator == null) {
            throw new NotFoundException("Калькулятор не найден");
        }
        return Calculator.toModel(calculator);
    }

    public Iterable<Calculator> getAll() {
        return Calculator.toModelList(calculatorRepository.findAll());
    }

    public CalculatorInfo getInfo(String name) throws NotFoundException {
        CalculatorEntity calculator = calculatorRepository.findByName(name);
        if (calculator == null) {
            throw new NotFoundException("Калькулятор не найден");
        }
        return CalculatorInfo.toModel(calculator);
    }

    public Long delete(Long id) throws NotFoundException {
        CalculatorEntity calculator = calculatorRepository.findById(id).get();
        if (calculator == null) {
            throw new NotFoundException("Калькулятор не найден");
        }
        calculatorRepository.deleteById(id);
        return id;
    }

    public Result getResult(String name, Map<String, String> parameters) throws NotFoundException, ParameterException {
        CalculatorEntity calculator = calculatorRepository.findByName(name);
        if (calculator == null) {
            throw new NotFoundException("Калькулятор не найден");
        }
        return switch (name){
            case "calculatorTitrationRate" -> (new CalculatorTitrations()).calculate(parameters);
            case "calculatorBodyMassIndex" -> (new CalculatorBodyMassIndex()).calculate(parameters);
            case "calculatorRateIntravenousDripDrug" -> (new CalculatorRateIntravenousDripDrug()).calculate(parameters);
            default -> throw new NotFoundException("Калькулятор не найден");
        };
    }

}