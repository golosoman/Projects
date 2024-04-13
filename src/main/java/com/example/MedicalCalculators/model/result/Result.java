package com.example.MedicalCalculators.model.result;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class Result {
    private String result;

    public static Result toModel(String string) {
        Result model = new Result();
        model.setResult(string);
        return model;
    }
}
