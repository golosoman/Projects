package com.example.MedicalCalculators.api.controller;

import com.example.MedicalCalculators.dto.request.typeCalculator.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.RIDDCalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorInfoFull;
import com.example.MedicalCalculators.dto.response.CalculatorInfo;
import com.example.MedicalCalculators.dto.request.CalculatorInfoRequest;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.service.CalculatorService.CalculatorService;
import org.springdoc.core.annotations.ParameterObject;
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
    @ResponseBody
    public CalculatorInfoFull get(@ParameterObject @PathVariable(name = "id") Long id) {
        return calculatorService.getOne(id);
    }

    @GetMapping
    @ResponseBody
    public List<CalculatorInfoFull> getAll() {
        return calculatorService.getAll();
    }

    @GetMapping("/{name}/info")
    @ResponseBody
    public CalculatorInfo getInfo(@PathVariable String name) {
        return calculatorService.getInfo(name);
    }

    @PostMapping("/body-mass-index/result")
    @ResponseBody
    public CalculatorResult BMIResult(@RequestBody BMICalculatorRequest calculatorRequest) {
        return calculatorService.getBMIResult(calculatorRequest);
    }

    @PostMapping("/titration-rate/result")
    @ResponseBody
    public CalculatorResult TitrationResult(@RequestBody TitrationCalculatorRequest calculatorRequest) {
        return calculatorService.getTitrationResult(calculatorRequest);
    }

    @PostMapping("/rate-intravenous-drip-drug/result")
    @ResponseBody
    public CalculatorResult TitrationResult(@RequestBody RIDDCalculatorRequest calculatorRequest) {
        return calculatorService.getRIDDResult(calculatorRequest);
    }
}