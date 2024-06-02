<template>
    <spin-loader v-if="isCalculatorsLoading" />
    <div v-else class="content mt-3">
        <calculator-list-card :calculators="calculatorsInfo" />
    </div>
</template>
<script lang="ts">
import { useCalculators } from '@/hooks/calculators/useCalculators'
import CalculatorListCard from '@/components/CalculatorListCard.vue'

export default {
    components: {
        CalculatorListCard
    },
    setup() {
        const { calculatorsInfo, isCalculatorsLoading } = useCalculators(3)
        console.log(calculatorsInfo)
        return { calculatorsInfo, isCalculatorsLoading }
    }
}
</script>
