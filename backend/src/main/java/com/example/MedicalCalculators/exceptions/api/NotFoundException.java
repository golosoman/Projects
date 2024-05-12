package com.example.MedicalCalculators.exceptions.api;


import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Getter;
import org.springframework.format.annotation.DateTimeFormat;

import java.util.Date;

@Getter
public class NotFoundException extends RuntimeException {
    @DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date timestamp;

    public NotFoundException(Date timestamp, String message) {
        super(message);
        this.timestamp = timestamp;
    }
}
