import axios from '@/axiosConfig'
import { ref, type Ref, onUpdated} from 'vue'
import type { ICalculatorResult } from '@/types/calculator';
export function useBMICalculator(weight: number, height: number) {
    // const calculatorResult: Ref<ICalculatorResult | null> = ref(null);

    const getResult = async() => {
        try {
            const response = await axios.post<ICalculatorResult>('/calculator/body-mass-index/result', {
                'weightPatient': weight,
                'height': height
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
