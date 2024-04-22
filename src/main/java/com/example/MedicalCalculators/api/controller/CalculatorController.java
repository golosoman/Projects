package com.example.MedicalCalculators.api.controller;

import com.example.MedicalCalculators.dto.request.typeCalculator.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.RIDDCalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorInfoFull;
import com.example.MedicalCalculators.dto.response.CalculatorInfo;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.service.CalculatorService.CalculatorService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.log4j.Log4j2;
import org.springdoc.core.annotations.ParameterObject;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/calculator")
@Log4j2
@Tag(
        name="Контроллер API калькуляторов",
        description="Позволяет получить информацию о медицинских калькуляторах"
)
public class CalculatorController {
    private final CalculatorService calculatorService;

    public CalculatorController(CalculatorService calculatorService) {
        this.calculatorService = calculatorService;
        log.info("CalculatorController has been created");
    }

    @GetMapping("/{id}")
    @ResponseBody
    @Operation(
            summary = "Получить калькулятор по его id",
            description = "Позволяет получить полную информацию о калькуляторе по его идентификатору id. " +
                    "Информация включает: id - идентификатор калькулятора, name - название калькулятора и " +
                    "description - описание калькулятора"
    )
    public CalculatorInfoFull get(@PathVariable(name = "id" )
                                      @Parameter(description = "Идентификатор калькулятора") Long id) {
        log.info("Request GET to the address: /calculator/" + id);
        return calculatorService.getOne(id);
    }

    @GetMapping
    @ResponseBody
    @Operation(
            summary = "Получить список доступных калькуляторов",
            description = "Позволяет получить полную информацию о все калькуляторах, которые можно использовать. " +
                    "Информация включает: id - идентификатор калькулятора, name - название калькулятора " +
                    "и description - описание калькулятора"
    )
    public List<CalculatorInfoFull> getAll() {
        log.info("Request GET to the address: /calculator");
        return calculatorService.getAll();
    }

    @GetMapping("/{name}/info")
    @ResponseBody
    @Operation(
            summary = "Получение информацию о калькуляторе по его названию",
            description = "Позволяет получить описание калькулятора по его названию name. Описание включает: " +
                    "info - описание калькулятора"
    )
    public CalculatorInfo getInfo(@PathVariable(name="name")
                                      @Parameter(description = "Название калькулятора") String name) {
        log.info("Request GET to the address: /calculator/" + name + "/info");
        return calculatorService.getInfo(name);
    }

    @PostMapping("/body-mass-index/result")
    @ResponseBody
    @Operation(
            summary = "Получение результата вычисления для калькулятора индекса массы тела",
            description = "Позволяет получить результат вычисления для калькулятора индекса массы тела. " +
                    "Результат включает: result - результат вычисления в кг/м²"
    )
    public CalculatorResult BMIResult(@RequestBody BMICalculatorRequest calculatorRequest) {
        log.info("Request POST to the address: /body-mass-index/result");
        return calculatorService.getBMIResult(calculatorRequest);
    }

    @PostMapping("/titration-rate/result")
    @ResponseBody
    @Operation(
            summary = "Получение результата вычисления для калькулятора расчета скорости инфузии препарата " +
                    "через линеомат(скорость титрования)",
            description = "Позволяет получить результат вычисления для калькулятора расчета скорости инфузии " +
                    "препарата через линеомат(скорость титрования). Результат включает: " +
                    "result - результат вычисления в мл/час"
    )
    public CalculatorResult TitrationResult(@RequestBody TitrationCalculatorRequest calculatorRequest) {
        log.info("Request POST to the address: /titration-rate/result");
        return calculatorService.getTitrationResult(calculatorRequest);
    }

    @PostMapping("/rate-intravenous-drip-drug/result")
    @ResponseBody
    @Operation(
            summary = "Получение результата вычисления для калькулятора расчета скорости внутривенного " +
                    "введения препарата",
            description = "Позволяет получить результат вычисления для калькулятора расчета скорости " +
                    "внутривенного введения препарата Результат включает: result - результат " +
                    "вычисления в каплях в минуту"
    )
    public CalculatorResult TitrationResult(@RequestBody RIDDCalculatorRequest calculatorRequest) {
        log.info("Request POST to the address: /rate-intravenous-drip-drug/result");
        return calculatorService.getRIDDResult(calculatorRequest);
    }
}