package com.example.MedicalCalculators.api.controller;

import com.example.MedicalCalculators.entity.CalculatorEntity;
import com.example.MedicalCalculators.exceptions.CalculatorAlreadyExistsException;
import com.example.MedicalCalculators.exceptions.CalculatorNotFoundException;
import com.example.MedicalCalculators.service.CalculatorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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
        } catch (CalculatorAlreadyExistsException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e){
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

    @GetMapping
    public ResponseEntity getAll(){
        try {
            return ResponseEntity.ok(calculatorService.getAll());
        } catch (Exception e){
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity getOne(@PathVariable Long id){
        try {
            return ResponseEntity.ok(calculatorService.getOne(id));
        } catch (CalculatorNotFoundException e){
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e){
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }

//    @GetMapping
//    public ResponseEntity getByName(@RequestParam String calculatorName){
//        try {
//            return ResponseEntity.ok(calculatorService.getByName(calculatorName));
//        } catch (CalculatorNotFoundException e){
//            return ResponseEntity.badRequest().body(e.getMessage());
//        } catch (Exception e){
//            return ResponseEntity.badRequest().body("Произошла ошибка");
//        }
//    }

    @DeleteMapping("/{id}")
    public ResponseEntity delete(@PathVariable Long id){
        try {
            return ResponseEntity.ok(calculatorService.delete(id));
        } catch (Exception e){
            return ResponseEntity.badRequest().body("Произошла ошибка");
        }
    }
}