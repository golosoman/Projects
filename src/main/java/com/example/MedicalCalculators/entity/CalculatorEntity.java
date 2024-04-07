package com.example.MedicalCalculators.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class CalculatorEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private String description;
    private String formula;

    @ManyToMany
    @JoinTable(
            name = "CalculatorParameter",
            joinColumns = @JoinColumn(name = "calculator_id"),
            inverseJoinColumns = @JoinColumn(name = "parameter_id")
    )
    private List<ParameterEntity> parameter;
}
