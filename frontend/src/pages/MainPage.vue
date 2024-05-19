<template>
    <div class="content">
        <h1>Ну типо привет!</h1>
        <calculator-list-card :calculators="calculatorsInfo" />
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
        const {calculatorsInfo} = useCalculators(3)
        console.log(calculatorsInfo) 
        return { calculatorsInfo }
    }
}
</script>
