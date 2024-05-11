import * as yup from 'yup'

export const messageSchema = yup.object().shape({
    message: yup.string().min(1, 'Комментарий не должен быть пустым!')
})
