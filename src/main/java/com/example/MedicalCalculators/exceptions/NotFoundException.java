package com.example.MedicalCalculators.exceptions;

import java.io.Serial;

public class NotFoundException extends RuntimeException {
    public NotFoundException(String message) {
        super(message);
    }
}
