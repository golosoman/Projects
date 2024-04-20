package com.example.MedicalCalculators.dto.request;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@AllArgsConstructor
public class CalculatorInfoRequest {
    private String name;
    private String description;
}