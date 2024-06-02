import axios from '@/axiosConfig'
import baseAxios from 'axios'
import type { ICalculatorResult } from '@/types/calculator'
export function useTitrationCalculator(
    amount: number,
    volume: number,
    weight: number,
    dosage: number
) {
    const getResult = async () => {
        try {
            const response = await axios.post<ICalculatorResult>(
                '/calculator/titration-rate/result',
                {
                    amountOfDrug: amount,
                    volumeOfSolution: volume,
                    weightPatient: weight,
                    dosage: dosage,
                    isMlInHour: true
                }
            )
            return response.data
        } catch (error) {
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
