package com.example.MedicalCalculators.exceptions.api;

import lombok.extern.log4j.Log4j2;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;

@RestControllerAdvice
@Log4j2
public class ExceptionApiHandler {
    @ExceptionHandler(NotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorMessage notFoundException(NotFoundException exception, WebRequest request) {
        ErrorMessage message = new ErrorMessage(
                HttpStatus.NOT_FOUND.value(),
                exception.getTimestamp(), // Используйте timestamp из исключения
                exception.getMessage(),
                request.getDescription(false)
        );
        log.error(message.getMessage());
        return message;
    }

    @ExceptionHandler(AlreadyExistsException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public ErrorMessage alreadyExistsException(AlreadyExistsException exception, WebRequest request) {
        ErrorMessage message = new ErrorMessage(
                HttpStatus.FORBIDDEN.value(),
                exception.getTimestamp(), // Используйте timestamp из исключения
                exception.getMessage(),
                request.getDescription(false)
        );
        log.error(message.getMessage());
        return message;
    }
}
