import axios from '@/axiosConfig'
import type { IInfo } from '@/types/calculator'
import { ref, type Ref, onMounted } from 'vue'

export function useCalculator(name: string) {
    const calculatorInfo: Ref<IInfo | null> = ref(null)
    const isCalculatorLoading: Ref<boolean> = ref(true)

    const getInfo = async () => {
        try {
            const response = await axios.get<IInfo>(`/calculator/${name}/info`)
            calculatorInfo.value = response.data
        } catch (error) {
            console.log(error)
        } finally {
            isCalculatorLoading.value = false
        }
    }

    onMounted(() => {
        getInfo()
    })
    return { calculatorInfo, isCalculatorLoading }
}
