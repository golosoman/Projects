import * as yup from 'yup'

export const authSchema = yup.object().shape({
    password: yup
        .string()
        .required('Пожалуйста, укажите пароль')
        .min(8, 'Пароль должен быть не менее 8 символов'),
    email: yup
        .string()
        .required('Пожалуйста, укажите адрес электронной почты')
        .email('Пожалуйста, укажите действительный адрес электронной почты')
})
