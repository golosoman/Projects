<script lang="ts">
import { onMounted, onUpdated, ref, type Ref } from 'vue'
import { useBMICalculator } from '@/hooks/calculators/useBMICalculator'
import { useCalculator } from '@/hooks/calculators/useCalculator'
export default {
    setup(props, ctx) {
        let body_weight: Ref<string> = ref('')
        let body_height: Ref<string> = ref('')
        let result: Ref<string> = ref('')
        let textRecommendation: Ref<string> = ref('')

        const { calculatorInfo, isCalculatorLoading } = useCalculator('body-mass-index')

        const calculate_result = async () => {
            try {
                const { getResult } = useBMICalculator(
                    Number(body_weight.value),
                    Number(body_height.value)
                )
                result.value = String((await getResult())?.result)
                recommendation()
                clearForm()
            } catch (error) {
                console.log(error)
            }
        }

        const clearForm = () => {
            body_weight.value = ''
            body_height.value = ''
        }

        const recommendation = () => {
            let currentResult = parseFloat(result.value);
            console.log(result.value)
            if (currentResult <= 16) {
                textRecommendation.value = 'Выраженный дефицит массы тела'
            } else if (currentResult <= 18.5) {
                textRecommendation.value = 'Недостаточная (дефицит) масса тела'
            } else if (currentResult <= 25) {
                textRecommendation.value = 'Норма'
            } else if (currentResult <= 30) {
                textRecommendation.value = 'Избыточная масса тела (предожирение)'
            } else if (currentResult <= 35) {
                textRecommendation.value = 'Ожирение первой степени'
            } else if (currentResult <= 40) {
                textRecommendation.value = 'Ожирение второй степени'
            }else if (currentResult > 40) {
                textRecommendation.value = 'Ожирение третьей степени (морбидное)'
            } else {
                textRecommendation.value = 'Невозможно интерпретировать результат'
            }
        }

        return {
            body_weight,
            body_height,
            result,
            calculatorInfo,
            isCalculatorLoading,
            calculate_result,
            textRecommendation: textRecommendation,
            clearForm,
            recommendation
        }
    }
}
</script>
<template>
    <div class="content border border-1 border-secondary rounded-3 p-3 mx-5 my-3">
        <h1 class="text-center">Калькулятор для расчета индекса массы тела</h1>
        <div class="content row d-flex justify-content-between">
            <div class="content w-75 row">
                <div class="col-6 px-5 py-2 mb-3">
                    <form @submit.prevent>
                        <base-input
                            labelText="Масса тела, кг"
                            inputType="number"
                            inputPlaceholder="Введите массу тела:"
                            v-model="body_weight"
                            class="mt-4 mb-4"
                        />
                        <base-input
                            labelText="Рост, см"
                            inputType="number"
                            inputPlaceholder="Введите рост:"
                            v-model="body_height"
                            class="mt-4 mb-4"
                        />
                        <div class="d-flex justify-content-center">
                            <base-button @click="calculate_result" class="mx-1"
                                >Рассчитать</base-button
                            >
                            <base-button @click="clearForm" class="mx-1">Сбросить</base-button>
                        </div>
                    </form>
                </div>
                <div class="content col-6 row my-auto h-50 w-50 border pb-3 bg-light bg-gradient">
                    <div class="col-12 my-auto border">Результат вычисления: {{ result }} в кг/м²</div>
                    <div class="col-12 border">Рекомендация: {{ textRecommendation }}</div>
                </div>
            </div>
        </div>

        <div class="content px-3">
            <div class="content">
                <h2>Об калькуляторе</h2>
                <p>
                    {{ calculatorInfo?.info.split('.')[0] + '.' }}
                </p>
            </div>
            <div class="content">
                <h2>Формула</h2>
                <img
                    src="../../static/image/calculators/body_mass_index/formula.png"
                    width=""
                    alt="Формула"
                    class="d-inline-block align-middle mr-2"
                />
                <p class="mt-2">
                    где: m — масса тела в килограммах; h — рост в метрах; измеряется в кг/м².
                    <br /><br />
                    Калькулятор рачитывает показатели в следующих интервалах: рост не более 300 см;
                    вес не менее 10 кг.
                    <br /><br />
                    Возможен ввод дробных значений веса с точность до одного знака после запятой.
                </p>
            </div>
            <div class="content">
                <h2>Интерпретация</h2>
                <p>
                    В соответствии с рекомендациями ВОЗ разработана следующая интерпретация
                    показателей ИМТ:
                </p>
                <img
                    src="../../static/image/calculators/body_mass_index/table.png"
                    width=""
                    alt="Таблица"
                    class="d-inline-block align-middle mr-2"
                />
            </div>
            <div class="content mt-2">
                <h2>Дополнительные сведения</h2>
                <p>
                    Целесообразно рассчитывать индекс массы тела для лиц старше 19 лет.
                    <br /><br />
                    Индекс массы тела следует применять с осторожностью, исключительно для
                    ориентировочной оценки — например, попытка оценить с его помощью телосложение
                    профессиональных спортсменов может дать неверный результат (высокое значение
                    индекса в этом случае объясняется развитой мускулатурой). Поэтому для более
                    точной оценки степени накопления жира наряду с индексом массы тела целесообразно
                    определять также индексы центрального ожирения.
                    <br /><br />
                    Показатель индекса массы тела разработан бельгийским социологом и статистиком
                    Адольфом Кетеле (Adolphe Quetelet) в 1869 году.
                </p>
            </div>
        </div>
    </div>
</template>
