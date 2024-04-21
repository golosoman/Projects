package com.example.MedicalCalculators.service.CalculatorService.typeCalculator;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum CalculatorType {
    BODY_MASS_INDEX ("body-mass-index"),
    RATE_INTRAVENOUS_DRIP_DRUG ("rate-intravenous-drip-drug"),
    TITRATIONS("titration-rate");

    private final String name;

    public int getId() {
        return ordinal() + 1;
    }
}
