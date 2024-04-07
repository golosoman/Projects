package com.example.MedicalCalculators.api.controller;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import com.example.MedicalCalculators.entity.ParameterEntity;
import com.example.MedicalCalculators.exceptions.AlreadyExistsException;
import com.example.MedicalCalculators.exceptions.NotFoundException;
import com.example.MedicalCalculators.service.CalculatorService;
import com.example.MedicalCalculators.service.ParameterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/parameter")
public class ParameterController {
    @Autowired
    private ParameterService parameterService;

    @PostMapping
    public ResponseEntity add(@RequestBody ParameterEntity parameter) {
        try {
            parameterService.add(parameter);
            return ResponseEntity.ok("Параметр успешно создан");
        } catch (AlreadyExistsException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

    @GetMapping
    public ResponseEntity getAll() {
        try {
            return ResponseEntity.ok(parameterService.getAll());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity getOne(@PathVariable Long id) {
        try {
            return ResponseEntity.ok(parameterService.getOne(id));
        } catch (NotFoundException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity delete(@PathVariable Long id) {
        try {
            return ResponseEntity.ok(parameterService.delete(id));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }
}
