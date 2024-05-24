<template>
    <spin-loader v-if="isCalculatorLoading" />
    <div v-else class="content mt-3">
        <calculator-list-card  :calculators="calculatorsInfo" />
    </div>
</template>
<script>
import { useCalculators } from '@/hooks/calculators/useCalculators'
import CalculatorListCard from '@/components/CalculatorListCard.vue'

export default {
    components: {
        CalculatorListCard
    },
    setup() {
        const {calculatorsInfo, isCalculatorLoading } = useCalculators(3)
        console.log(calculatorsInfo) 
        return { calculatorsInfo, isCalculatorLoading }
    }
}
</script>
