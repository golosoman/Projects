<template>
    <div class="card-deck d-flex justify-content-around">
        <CalculatorCard
            v-for="calculator in calculators"
            :calculator="calculator"
            :key="calculator.id"
        />
    </div>
</template>
<script setup lang="ts">
import CalculatorCard from './CalculatorCard.vue'
import { defineProps } from 'vue'
import { type ICalculatorInfo } from '@/types/calculator'

const props = defineProps({
    calculators: {
        type: Array<ICalculatorInfo>,
        required: true
    }
})
</script>
