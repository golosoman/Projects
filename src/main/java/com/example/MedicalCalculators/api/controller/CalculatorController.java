package com.example.MedicalCalculators.api.controller;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import com.example.MedicalCalculators.exceptions.AlreadyExistsException;
import com.example.MedicalCalculators.exceptions.NotFoundException;
import com.example.MedicalCalculators.exceptions.ParameterException;
import com.example.MedicalCalculators.service.CalculatorService.CalculatorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/calculator")
public class CalculatorController {
    @Autowired
    private CalculatorService calculatorService;

    @PostMapping
    public ResponseEntity add(@RequestBody CalculatorEntity calculator) {
        try {
            calculatorService.add(calculator);
            return ResponseEntity.ok("Калькулятор успешно создан");
        } catch (AlreadyExistsException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

    @GetMapping
    public ResponseEntity getAll() {
        try {
            return ResponseEntity.ok(calculatorService.getAll());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity getOne(@PathVariable Long id) {
        try {
            return ResponseEntity.ok(calculatorService.getOne(id));
        } catch (NotFoundException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity delete(@PathVariable Long id) {
        try {
            return ResponseEntity.ok(calculatorService.delete(id));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

    @GetMapping("/{name}/info")
    public ResponseEntity getInfo(@PathVariable String name){
        try{
            return ResponseEntity.ok(calculatorService.getInfo(name));
        } catch (NotFoundException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

    @PostMapping("/{name}/result")
    public ResponseEntity getResult(@PathVariable String name, @RequestBody Map<String, String> parameters){
        try{
            return ResponseEntity.ok(calculatorService.getResult(name, parameters));
        } catch (NotFoundException | ParameterException  e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }
}