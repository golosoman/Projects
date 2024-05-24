import axios from '@/axiosConfig'
import type { ICalculatorResult } from '@/types/calculator';
export function useTitrationCalculator(amount: number, volume: number, weight: number, dosage: number) {

    const getResult = async() => {
        try {
            const response = await axios.post<ICalculatorResult>('/calculator/titration-rate/result', {
                "amountOfDrug": amount,
                "volumeOfSolution": volume,
                "weightPatient": weight,
                "dosage": dosage,
                "isMlInHour": true
            })
            // calculatorResult.value = response.data;
            return response.data
            console.log(response.data)
        } catch (error) {
            console.log(error);
        }
    }
    return {getResult}
}
