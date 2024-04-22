package com.example.MedicalCalculators.api.controller;

import com.example.MedicalCalculators.dto.request.typeCalculator.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.RIDDCalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorInfoFull;
import com.example.MedicalCalculators.dto.response.CalculatorInfo;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.service.CalculatorService.CalculatorService;
import lombok.extern.log4j.Log4j2;
import org.springdoc.core.annotations.ParameterObject;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/calculator")
@Log4j2
public class CalculatorController {
    private final CalculatorService calculatorService;

    public CalculatorController(CalculatorService calculatorService) {
        this.calculatorService = calculatorService;
        log.info("CalculatorController has been created");
    }

    @GetMapping("/{id}")
    @ResponseBody
    public CalculatorInfoFull get(@ParameterObject @PathVariable(name = "id") Long id) {
        log.info("Request GET to the address: /calculator/" + id);
        return calculatorService.getOne(id);
    }

    @GetMapping
    @ResponseBody
    public List<CalculatorInfoFull> getAll() {
        log.info("Request GET to the address: /calculator");
        return calculatorService.getAll();
    }

    @GetMapping("/{name}/info")
    @ResponseBody
    public CalculatorInfo getInfo(@PathVariable String name) {
        log.info("Request GET to the address: /calculator/" + name + "/info");
        return calculatorService.getInfo(name);
    }

    @PostMapping("/body-mass-index/result")
    @ResponseBody
    public CalculatorResult BMIResult(@RequestBody BMICalculatorRequest calculatorRequest) {
        log.info("Request POST to the address: /body-mass-index/result");
        return calculatorService.getBMIResult(calculatorRequest);
    }

    @PostMapping("/titration-rate/result")
    @ResponseBody
    public CalculatorResult TitrationResult(@RequestBody TitrationCalculatorRequest calculatorRequest) {
        log.info("Request POST to the address: /titration-rate/result");
        return calculatorService.getTitrationResult(calculatorRequest);
    }

    @PostMapping("/rate-intravenous-drip-drug/result")
    @ResponseBody
    public CalculatorResult TitrationResult(@RequestBody RIDDCalculatorRequest calculatorRequest) {
        log.info("Request POST to the address: /rate-intravenous-drip-drug/result");
        return calculatorService.getRIDDResult(calculatorRequest);
    }
}