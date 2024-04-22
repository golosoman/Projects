package com.example.MedicalCalculators;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;

@OpenAPIDefinition(
        info = @Info(
                title = "Medical Calculators",
                description = "API сервиса \"медицинские калькуляторы\"", version = "1.0.0",
                contact = @Contact(
                        name = "Лапин Константин Сергеевич",
                        email = "constan.lapin2015@mail.ru",
                        url = "https://t.me/Golosoman"
                )
        )
)
public class OpenApiConfig {
}
