import * as yup from 'yup'

const fileSchema = yup.mixed().test({
    name: 'fileSize',
    message: 'Файл слишком большой',
    test: (value) => value && value.size <= 1000000
})

const imageSchema = fileSchema.test({
    name: 'fileType',
    message: 'Неверный тип файла',
    test: (value) => value && ['image/jpeg', 'image/png', 'image/gif'].includes(value.type)
})

export const postSchema = yup.object().shape({
    image: imageSchema,
    content: yup
        .string()
        .required('Пожалуйста напишите что-то в содержимое поста')
        .min(6, 'Содержимое содержит минимум 6 символов'),
    title: yup
        .string()
        .required('Пожалуйста, укажите заголовок поста')
        .min(6, 'Заголовок содержит минимум 6 символов')
})
