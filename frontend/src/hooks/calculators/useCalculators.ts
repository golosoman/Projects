import axios from '@/axiosConfig'
import type { ICalculatorInfo } from '@/types/calculator'
import { ref, type Ref, onMounted } from 'vue'

export function useCalculators(n: number) {
    const calculatorsInfo: Ref<Array<ICalculatorInfo>> = ref([])

    const getAllInfo = async () => {
        try {
            for (let id = 1; id <= n; id++) {
                const response = await axios.get(`/calculator/${id}`)
                const calculator: ICalculatorInfo = response.data
                // console.log(calculator)
                calculatorsInfo.value.push(calculator)
            }
        } catch (error) {
            console.log(error)
        }
    }

    onMounted(() => {
        getAllInfo()
    })
    return {calculatorsInfo}
}
