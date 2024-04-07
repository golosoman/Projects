package com.example.MedicalCalculators.service;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import com.example.MedicalCalculators.exceptions.CalculatorAlreadyExistsException;
import com.example.MedicalCalculators.exceptions.CalculatorNotFoundException;
import com.example.MedicalCalculators.repository.CalculatorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CalculatorService {
    @Autowired
    private CalculatorRepository calculatorRepository;
    public CalculatorEntity add(CalculatorEntity calculator) throws CalculatorAlreadyExistsException {
        if(calculatorRepository.findByName(calculator.getName()) != null){
            throw new CalculatorAlreadyExistsException("Калькулятор с таким именем уже существует");
        }
        return calculatorRepository.save(calculator);
    }

    public CalculatorEntity getOne(Long id) throws CalculatorNotFoundException {
        CalculatorEntity calculator = calculatorRepository.findById(id).get();
        if(calculator == null){
            throw new CalculatorNotFoundException("Калькулятор не найден");
        }
        return calculator;
    }

//    public CalculatorEntity getByName(String name) throws CalculatorNotFoundException {
//        CalculatorEntity calculator = calculatorRepo.findByName(name);
//        if(calculator == null){
//            throw new CalculatorNotFoundException("Калькулятор не найден");
//        }
//        return calculator;
//    }

    public Iterable<CalculatorEntity> getAll() {
        return calculatorRepository.findAll();
    }

    public Long delete(Long id){
        calculatorRepository.deleteById(id);
        return id;
    }
}