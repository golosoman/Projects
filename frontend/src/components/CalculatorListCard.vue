<template> 
    <div class="card-deck d-flex justify-content-around">
        <CalculatorCard
            v-for="calculator in calculators"
            :calculator="calculator"
            :key="calculator.id"
        />
    </div>
</template>
<script setup>
import CalculatorCard from "./CalculatorCard.vue";
import {defineProps} from "vue"

const props = defineProps({
    calculators: {
        type: Array,
        required: true
    }
})

</script>
