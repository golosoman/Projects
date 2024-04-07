package com.example.MedicalCalculators.service;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import com.example.MedicalCalculators.exceptions.AlreadyExistsException;
import com.example.MedicalCalculators.exceptions.NotFoundException;
import com.example.MedicalCalculators.model.Calculator;
import com.example.MedicalCalculators.repository.CalculatorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

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

    public Long delete(Long id) throws NotFoundException {
        CalculatorEntity calculator = calculatorRepository.findById(id).get();
        if (calculator == null) {
            throw new NotFoundException("Калькулятор не найден");
        }
        calculatorRepository.deleteById(id);
        return id;
    }
}