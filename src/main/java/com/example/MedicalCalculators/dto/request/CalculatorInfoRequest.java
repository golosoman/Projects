package com.example.MedicalCalculators.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class CalculatorInfoRequest {
    private String name;
    private String description;
}