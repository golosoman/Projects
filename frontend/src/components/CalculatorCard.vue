<template>
    <div class="card w-25">
        <img :src="setImage(calculator.name)" class="card-img-top" alt="Картинка калькулятора" />
        <div class="card-body">
            <a
                :href="'/calculator/' + calculator.name"
                class="card-title link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover"
                >{{ changeName(props.calculator.name) }}</a
            >
            {{ console.log(props.calculator) }}
            <p class="card-text">
                {{ truncateWords(props.calculator.info, 5) }}
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
// import { ICalculatorInfo } from '@/types/calculator'
import { defineProps } from 'vue'
import { type ICalculatorInfo } from '@/types/calculator'

const props = defineProps<{
    calculator: ICalculatorInfo
}>()
interface DictNamesType {
    [key: string]: {
        name: string
        img: string
    }
}

const dictNames: DictNamesType = {
    'body-mass-index': {
        name: 'Индекс массы тела',
        img: 'src/static/image/calculators/body_mass_index/body_mass_index.jpg'
    },
    'rate-intravenous-drip-drug': {
        name: 'Скорость внутривенного капельного введения препарата',
        img: 'src/static/image/calculators/rate_intravenous_drip_drug/rate_intravenous_drip_drug.jpg'
    },
    'titration-rate': {
        name: 'Скорость инфузии препарата',
        img: 'src/static/image/calculators/titration_rate/titration_rate.jpg'
    }
}

const setImage = (name: string) => {
    let src = '...'
    if (name in dictNames) {
        src = dictNames[name].img
    }

    return src
}

const changeName = (name: string) => {
    if (name in dictNames) {
        name = dictNames[name].name
    }

    return name
}

// Фильтр для усечения строки по словам и добавления многоточия
const truncateWords = (value: string, wordCount: number) => {
    if (!value) return ''
    const words = value.split(' ')
    return words.length <= wordCount ? value : words.slice(0, wordCount).join(' ') + '...'
}
</script>
