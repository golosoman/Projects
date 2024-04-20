package com.example.MedicalCalculators.dto.response;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class CalculatorInfoFull {
    private Long id;
    private String name;
    private String description;
}
