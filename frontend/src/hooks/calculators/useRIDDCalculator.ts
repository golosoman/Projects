import axios from '@/axiosConfig'
import type { ICalculatorResult } from '@/types/calculator';
export function useRIDDCalculator(volume: number, time: number) {

    const getResult = async() => {
        try {
            const response = await axios.post<ICalculatorResult>('/calculator/rate-intravenous-drip-drug/result', {
                'volumeOfSolution': volume,
                'timeTaking': time,
                'isMinute': true
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
