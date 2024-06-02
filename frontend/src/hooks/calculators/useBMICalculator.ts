import axios from '@/axiosConfig'
import baseAxios from 'axios'
import type { ICalculatorResult } from '@/types/calculator'
export function useBMICalculator(weight: number, height: number) {
    // const calculatorResult: Ref<ICalculatorResult | null> = ref(null);

    const getResult = async () => {
        try {
            const response = await axios.post<ICalculatorResult>(
                '/calculator/body-mass-index/result',
                {
                    weightPatient: weight,
                    height: height
                }
            )
            return response.data
        } catch (error: any) {
            if (baseAxios.isAxiosError(error)) {
                throw error
            } else if (error instanceof Error) {
                console.log(error)
            } else {
                console.log('An unknown error occurred')
            }
        }
    }
    return { getResult }
}
