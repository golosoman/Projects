import axios from '@/axiosConfig'
import baseAxios from 'axios'
import type { ICalculatorResult } from '@/types/calculator'
export function useRIDDCalculator(volume: number, time: number) {
    const getResult = async () => {
        try {
            const response = await axios.post<ICalculatorResult>(
                '/calculator/rate-intravenous-drip-drug/result',
                {
                    volumeOfSolution: volume,
                    timeTaking: time,
                    isMinute: true
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
