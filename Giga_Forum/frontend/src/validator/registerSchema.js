import * as yup from 'yup'

export const registerSchema = yup.object().shape({
    confirmPassword: yup
        .string()
        .oneOf([yup.ref('password'), null], 'Пароли не совпадают')
        .required(),

    password: yup
        .string()
        .required('Пожалуйста, укажите пароль')
        .min(8, 'Пароль должен быть не менее 8 символов'),
    email: yup
        .string()
        .required('Пожалуйста, укажите адрес электронной почты')
        .email('Пожалуйста, укажите действительный адрес электронной почты'),
    name: yup
        .string()
        .required('Пожалуйста укажите ваш ник')
        .min(4, 'Ник должен содержать минимум 4 символа')
})
