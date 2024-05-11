package com.example.MedicalCalculators;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class MedicalCalculatorsApplication {
    public static void main(String[] args) {
        SpringApplication.run(MedicalCalculatorsApplication.class, args);
    }

}
