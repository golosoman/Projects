package com.example.MedicalCalculators.exceptions;

public class AlreadyExistsException extends IllegalArgumentException {
    public AlreadyExistsException(String message) {
        super(message);
    }
}
