package com.example.MedicalCalculators.exceptions.api;

public class AlreadyExistsException extends IllegalArgumentException {
    public AlreadyExistsException(String message) {
        super(message);
    }
}
