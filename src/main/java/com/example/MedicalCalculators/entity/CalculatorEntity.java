package com.example.MedicalCalculators.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.Collection;
import java.util.List;
import java.util.Set;

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

//    @ManyToMany(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
//    @JoinTable(
//            name = "CalculatorParameter",
//            joinColumns = {@JoinColumn(name = "calculator_id", referencedColumnName = "id")},
//            inverseJoinColumns = {@JoinColumn(name = "parameter_id", referencedColumnName = "id")}
//    )
//    private Set<ParameterEntity> parameter;
}
