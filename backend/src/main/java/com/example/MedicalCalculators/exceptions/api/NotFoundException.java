package com.example.MedicalCalculators.exceptions.api;


public class NotFoundException extends RuntimeException {
    public NotFoundException(String message) {
        super(message);
    }
}
