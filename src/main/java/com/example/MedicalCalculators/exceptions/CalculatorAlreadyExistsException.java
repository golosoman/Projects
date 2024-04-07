package com.example.MedicalCalculators.exceptions;

public class CalculatorAlreadyExistsException extends Exception{
    public CalculatorAlreadyExistsException(String message){
        super(message);
    }
}
