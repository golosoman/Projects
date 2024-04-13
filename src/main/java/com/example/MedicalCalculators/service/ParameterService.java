package com.example.MedicalCalculators.service;

import com.example.MedicalCalculators.entity.ParameterEntity;
import com.example.MedicalCalculators.exceptions.AlreadyExistsException;
import com.example.MedicalCalculators.exceptions.NotFoundException;
import com.example.MedicalCalculators.model.parameter.Parameter;
import com.example.MedicalCalculators.repository.ParameterRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ParameterService {
    @Autowired
    private ParameterRepository parameterRepository;

    public ParameterEntity add(ParameterEntity parameter) throws AlreadyExistsException {
        if (parameterRepository.findByName(parameter.getName()) != null) {
            throw new AlreadyExistsException("Параметр с таким именем уже существует");
        }
        return parameterRepository.save(parameter);
    }

    public Parameter getOne(Long id) throws NotFoundException {
        ParameterEntity parameter = parameterRepository.findById(id).get();
        if (parameter == null) {
            throw new NotFoundException("Параметр не найден");
        }
        return Parameter.toModel(parameter);
    }

    public Iterable<Parameter> getAll() {
        return Parameter.toModelList(parameterRepository.findAll());
    }

    public Long delete(Long id) throws NotFoundException {
        ParameterEntity parameter = parameterRepository.findById(id).get();
        if (parameter == null) {
            throw new NotFoundException("Параметр не найден");
        }
        parameterRepository.deleteById(id);
        return id;
    }
}
