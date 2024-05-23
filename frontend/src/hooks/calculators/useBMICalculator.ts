import axios from '@/axiosConfig'
import { ref, type Ref, onMounted } from 'vue'

export function useBMICalculator(weight: number, height: number) {
    const calculatorResult: Ref<number> = ref(0);
    const getResult = async() => {
        try {
            const response = await axios.post('/calculator/body-mass-index/result', {
                'weightPatient': weight,
                'height': height
            })
            calculatorResult.value = response.data;
        } catch (error) {
            console.log(error);
        } 
    }
    onMounted(() => {
        getResult()
    })
    return {calculatorResult}
}
