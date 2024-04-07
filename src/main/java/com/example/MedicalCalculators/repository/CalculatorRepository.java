package com.example.MedicalCalculators.repository;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import org.springframework.data.repository.CrudRepository;

public interface CalculatorRepository extends CrudRepository<CalculatorEntity, Long> {
    CalculatorEntity findByName(String name);
}
