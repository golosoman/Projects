package com.example.MedicalCalculators.model.parameter;

import com.example.MedicalCalculators.entity.ParameterEntity;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
public class Parameter {
    Long id;
    String name;
    public static Parameter toModel(ParameterEntity entity) {
        Parameter model = new Parameter();
        model.setId(entity.getId());
        model.setName(entity.getName());
        return model;
    }

    public static List<Parameter> toModelList(Iterable<ParameterEntity> entities) {
        List<Parameter> list = new ArrayList<Parameter>();
        entities.forEach((entity) -> {
            Parameter model = Parameter.toModel(entity);
            list.add(model);
        });
        return list;
    }
}
