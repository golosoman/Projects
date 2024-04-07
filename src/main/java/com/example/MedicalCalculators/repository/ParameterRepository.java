package com.example.MedicalCalculators.repository;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import com.example.MedicalCalculators.entity.ParameterEntity;
import org.springframework.data.repository.CrudRepository;

public interface ParameterRepository extends CrudRepository<ParameterEntity, Long> {
    ParameterEntity findByName(String name);
}
