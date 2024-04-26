package com.example.MedicalCalculators.api.controller;

import com.example.MedicalCalculators.dto.request.typeCalculator.BMICalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.RIDDCalculatorRequest;
import com.example.MedicalCalculators.dto.request.typeCalculator.TitrationCalculatorRequest;
import com.example.MedicalCalculators.dto.response.CalculatorInfoFull;
import com.example.MedicalCalculators.dto.response.CalculatorInfo;
import com.example.MedicalCalculators.dto.response.CalculatorResult;
import com.example.MedicalCalculators.exceptions.api.ErrorMessage;
import com.example.MedicalCalculators.exceptions.validation.ValidationErrorResponse;
import com.example.MedicalCalculators.service.CalculatorService.CalculatorService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.log4j.Log4j2;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Log4j2
@Tag(
        name = "Контроллер API калькуляторов",
        description = "Позволяет получить информацию о медицинских калькуляторах, " +
                "а также результаты вычисления на основе принимаемых параметров"
)
@RestController
@RequestMapping("/calculator")
public class CalculatorController {
    private final CalculatorService calculatorService;

    public CalculatorController(CalculatorService calculatorService) {
        this.calculatorService = calculatorService;
        log.info("CalculatorController has been created");
    }

    @Operation(
            summary = "Получить калькулятор по его идентификатору",
            description = "Позволяет получить полную информацию о калькуляторе по его идентификатору \"id\". " +
                    "Информация включает: \"id\" - идентификатор калькулятора, \"name\" - название калькулятора и " +
                    "\"info\" - описание калькулятора"
    )
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200",
                    description = "Калькулятор был получен по его идентификатору id",
                    content = {@Content(mediaType = "application/json",
                            schema = @Schema(implementation = CalculatorInfoFull.class)
                    )}
            ),
            @ApiResponse(responseCode = "404",
                    description = "Калькулятор не был найден по его названию name",
                    content = {@Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorMessage.class),
                            examples = @ExampleObject(value = "{" +
                                    "   \"statusCode\": 404, " +
                                    "   \"timestamp\": \"2024-04-22T17:01:56.160+04:00\", " +
                                    "   \"message\": \"Calculator with ID 5 not found\", " +
                                    "   \"description\": \"Resolved " +
                                    "[сom.example.MedicalCalculators.exceptions.controller.NotFoundException: " +
                                    "Calculator with ID 5 not found]\"" +
                                    "}"
                            )
                    )}
            )
    })
    @GetMapping("/{id}")
    @ResponseBody
    public CalculatorInfoFull get(@PathVariable(name = "id")
                                  @Parameter(description = "Идентификатор калькулятора") Long id) {
        log.info("Request GET to the address: /calculator/" + id);
        return calculatorService.getOne(id);
    }

    @Operation(
            summary = "Получить список доступных калькуляторов",
            description = "Позволяет получить полную информацию о все калькуляторах, которые можно использовать. " +
                    "Информация включает список из: \"id\" - идентификатор калькулятора, \"name\" - " +
                    "название калькулятора и \"info\" - описание калькулятора"
    )
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200",
                    description = "Калькуляторы были получены",
                    content = {@Content(mediaType = "application/json",
                            array = @ArraySchema(schema = @Schema(implementation = CalculatorInfoFull.class))
                    )}
            )
    })
    @GetMapping
    @ResponseBody
    public List<CalculatorInfoFull> getAll() {
        log.info("Request GET to the address: /calculator");
        return calculatorService.getAll();
    }

    @Operation(
            summary = "Получение информацию о калькуляторе по его названию",
            description = "Позволяет получить описание калькулятора по его названию \"name\". Описание включает: " +
                    "\"info\" - описание калькулятора"
    )
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200",
                    description = "Был получен калькулятор по его названию name",
                    content = {@Content(mediaType = "application/json",
                            schema = @Schema(implementation = CalculatorInfo.class)
                    )}
            ),
            @ApiResponse(responseCode = "404",
                    description = "Калькулятор не был найден по его названию name",
                    content = {@Content(mediaType = "application/json",
                            schema = @Schema(implementation = ErrorMessage.class),
                            examples = @ExampleObject(value = "{" +
                                    "   \"statusCode\": 404, " +
                                    "   \"timestamp\": \"2024-04-22T17:01:56.160+04:00\", " +
                                    "   \"message\": \"Calculator with ID 5 not found\", " +
                                    "   \"description\": \"Resolved " +
                                    "[com.example.MedicalCalculators.exceptions.controller.NotFoundException: " +
                                    "Calculator with ID 5 not found]\"" +
                                    "}"
                            )
                    )}
            )
    })
    @GetMapping("/{name}/info")
    @ResponseBody
    public CalculatorInfo getInfo(@PathVariable(name = "name")
                                  @Parameter(description = "Название калькулятора") String name) {
        log.info("Request GET to the address: /calculator/" + name + "/info");
        return calculatorService.getInfo(name);
    }

    @Operation(
            summary = "Получение результата вычисления для калькулятора индекса массы тела",
            description = "Позволяет получить результат вычисления для калькулятора индекса массы тела. " +
                    "Результат включает: \"result\" - результат вычисления в кг/м²"
    )
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200",
                    description = "Был получен результат вычисления " +
                            "калькулятора индкса массы тела",
                    content = {@Content(mediaType = "application/json",
                            schema = @Schema(implementation = CalculatorResult.class),
                            examples = @ExampleObject(value = "{\"result\": 20.194}"
                            )
                    )}
            ),
            @ApiResponse(responseCode = "400",
                    description = "Неверно заданы параметры",
                    content = {@Content(mediaType = "application/json",
                            schema = @Schema(implementation = ValidationErrorResponse.class),
                            examples = @ExampleObject(value = "{" +
                                    "    \"statusCode\": 400," +
                                    "    \"timestamp\": \"2024-04-26T13:11:44.329+00:00\"," +
                                    "    \"violations\": [" +
                                    "        {" +
                                    "            \"fieldName\": \"The minimum weight value is 10 kg\"," +
                                    "            \"message\": \"getBMIResult.calculatorRequest.weightPatient\"" +
                                    "        }," +
                                    "        {" +
                                    "            \"fieldName\": \"The height cannot exceed 300 cm\"," +
                                    "            \"message\": \"getBMIResult.calculatorRequest.height\"" +
                                    "        }" +
                                    "    ]" +
                                    "}"
                            )
                    )}
            )
    })
    @PostMapping("/body-mass-index/result")
    @ResponseBody
    public CalculatorResult BMIResult(@RequestBody BMICalculatorRequest calculatorRequest) {
        log.info("Request POST to the address: /body-mass-index/result");
        return calculatorService.getBMIResult(calculatorRequest);
    }

    @Operation(
            summary = "Получение результата вычисления для калькулятора расчета скорости инфузии препарата " +
                    "через линеомат(скорость титрования)",
            description = "Позволяет получить результат вычисления для калькулятора расчета скорости инфузии " +
                    "препарата через линеомат(скорость титрования). Результат включает: " +
                    "\"result\" - результат вычисления в мкг/кг*мин"
    )
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200",
                    description = "Был получен результат вычисления " +
                            "калькулятора расчета скорости инфузии через ленеомат(скорость титрования)",
                    content = {@Content(mediaType = "application/json",
                            schema = @Schema(implementation = CalculatorResult.class),
                            examples = @ExampleObject(value = "{\"result\": 13.4}"
                            )
                    )}
            ),
            @ApiResponse(responseCode = "400",
                    description = "Неверно заданы параметры",
                    content = {@Content(mediaType = "application/json",
                            schema = @Schema(implementation = ValidationErrorResponse.class),
                            examples = @ExampleObject(value = "{" +
                                    "    \"statusCode\": 400," +
                                    "    \"timestamp\": \"2024-04-26T14:25:46.311+00:00\"," +
                                    "    \"violations\": [" +
                                    "        {" +
                                    "            \"fieldName\": \"getTitrationResult.calculatorRequest.dosage\"," +
                                    "            \"message\": \"The dosage value of the drug is strictly positive\"" +
                                    "        }," +
                                    "        {" +
                                    "            \"fieldName\": \"getTitrationResult.calculatorRequest.amountOfDrug\"," +
                                    "            \"message\": \"The value of the amount of the drug is strictly positive\"" +
                                    "        }," +
                                    "        {" +
                                    "            \"fieldName\": \"getTitrationResult.calculatorRequest.weightPatient\"," +
                                    "            \"message\": \"The weight value is strictly positive\"" +
                                    "        }," +
                                    "        {" +
                                    "            \"fieldName\": \"getTitrationResult.calculatorRequest.volumeOfSolution\"," +
                                    "            \"message\": \"The value of the total volume of the solution is strictly positive\"" +
                                    "        }" +
                                    "    ]" +
                                    "}"
                            )
                    )}
            )
    })
    @PostMapping("/titration-rate/result")
    @ResponseBody
    public CalculatorResult TitrationResult(@RequestBody TitrationCalculatorRequest calculatorRequest) {
        log.info("Request POST to the address: /titration-rate/result");
        return calculatorService.getTitrationResult(calculatorRequest);
    }

    @Operation(
            summary = "Получение результата вычисления для калькулятора расчета скорости внутривенного " +
                    "введения препарата",
            description = "Позволяет получить результат вычисления для калькулятора расчета скорости " +
                    "внутривенного введения препарата Результат включает: \"result\" - результат " +
                    "вычисления в каплях в минуту"
    )
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200",
                    description = "Был получен результат вычисления " +
                            "калькулятора расчета скорости внутривенного введения препарата",
                    content = {@Content(mediaType = "application/json",
                            schema = @Schema(implementation = CalculatorResult.class),
                            examples = @ExampleObject(value = "{\"result\": 0.7}"
                            )
                    )}
            ),
            @ApiResponse(responseCode = "400",
                    description = "Неверно заданы параметры",
                    content = {@Content(mediaType = "application/json",
                            schema = @Schema(implementation = ValidationErrorResponse.class),
                            examples = @ExampleObject(value = "{" +
                                    "    \"statusCode\": 400," +
                                    "    \"timestamp\": \"2024-04-26T14:31:57.825+00:00\"," +
                                    "    \"violations\": [" +
                                    "        {" +
                                    "            \"fieldName\": \"getRIDDResult.calculatorRequest.volumeOfSolution\"," +
                                    "            \"message\": \"The value of the solution volume is strictly positive\"" +
                                    "        }," +
                                    "        {" +
                                    "            \"fieldName\": \"getRIDDResult.calculatorRequest.timeTaking\"," +
                                    "            \"message\": \"The value of the desired drug administration time is strictly positive\"" +
                                    "        }" +
                                    "    ]" +
                                    "}"
                            )
                    )}
            )
    })
    @PostMapping("/rate-intravenous-drip-drug/result")
    @ResponseBody
    public CalculatorResult TitrationResult(@RequestBody RIDDCalculatorRequest calculatorRequest) {
        log.info("Request POST to the address: /rate-intravenous-drip-drug/result");
        return calculatorService.getRIDDResult(calculatorRequest);
    }
}