package com.example.MedicalCalculators.api.controller;

import com.example.MedicalCalculators.dto.request.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.request.RIDDCalculatorRequest;
import com.example.MedicalCalculators.dto.request.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorInfoFull;
import com.example.MedicalCalculators.dto.response.CalculatorInfo;
import com.example.MedicalCalculators.dto.request.CalculatorInfoRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.service.CalculatorService.CalculatorService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/calculator")
public class CalculatorController {
    private final CalculatorService calculatorService;
    public CalculatorController(CalculatorService calculatorService) {
        this.calculatorService = calculatorService;
    }

    @GetMapping("/{id}")
    public CalculatorInfoFull get(@PathVariable(name = "id") Long id){
        return calculatorService.getOne(id);
    }

    @PostMapping
    public CalculatorInfoFull add(@RequestBody CalculatorInfoRequest calculatorInfoRequest) {
        return calculatorService.add(calculatorInfoRequest);
    }

    @GetMapping
    public List<CalculatorInfoFull> getAll() {
        return calculatorService.getAll();
    }

    @DeleteMapping("/{id}")
    public CalculatorInfoFull delete(@PathVariable Long id) {
        return calculatorService.delete(id);
    }

    @PatchMapping("/{id}")
    public CalculatorInfoFull update(@PathVariable Long id,
                                     @RequestBody CalculatorInfoRequest calculatorInfoRequest){
        return calculatorService.update(id, calculatorInfoRequest);
    }

    @GetMapping("/{name}/info")
    public CalculatorInfo getInfo(@PathVariable String name){
        return calculatorService.getInfo(name);
    }

    @PostMapping("/BodyMassIndex/result")
    public CalculatorResult BMIResult(@RequestBody BMICalculatorRequest calculatorRequest){
        return calculatorService.getBMIResult(calculatorRequest);
    }

    @PostMapping("/TitrationRate/result")
    public CalculatorResult TitrationResult(@RequestBody TitrationCalculatorRequest calculatorRequest){
        return calculatorService.getTitrationResult(calculatorRequest);
    }

    @PostMapping("/RateIntravenousDripDrug/result")
    public CalculatorResult TitrationResult(@RequestBody RIDDCalculatorRequest calculatorRequest){
        return calculatorService.getRIDDResult(calculatorRequest);
    }
}