<script lang="ts">
import { ref, type Ref } from 'vue'
import { useTitrationCalculator } from '@/hooks/calculators/useTitrationCalculator'
import { useCalculator } from '@/hooks/calculators/useCalculator'
export default {
    setup(props, ctx) {
        let amount_drug = ref('')
        let volume = ref('')
        let weight_patient = ref('')
        let dosage = ref('')
        let result: Ref<string> = ref('')

        const { calculatorInfo, isCalculatorLoading } = useCalculator('titration-rate')
        
        const calculate_result = async () => {
            try {
                const { getResult } = useTitrationCalculator(
                    Number(amount_drug.value),
                    Number(volume.value),
                    Number(weight_patient.value),
                    Number(dosage.value),
                )
                result.value = String((await getResult())?.result)
                clearForm()
            } catch (error) {
                console.log(error)
            }
        }
        const clearForm = () => {
            amount_drug.value = ''
            volume.value = ''
            weight_patient.value = ''
            dosage.value = ''
        }

        return {
            amount_drug,
            volume,
            weight_patient,
            dosage,
            result,
            calculate_result,
            clearForm, calculatorInfo, isCalculatorLoading
        }
    }
}
</script>
<template>
    <div class="content border border-1 border-secondary rounded-3 p-3 mx-5 my-3">
        <h1 class="text-center">
            Калькулятор для расчет скорости инфузии препарата через линеомат (скорость титрования)
        </h1>
        <div class="content row d-flex justify-content-between">
            <div class="content w-75 row">
                <div class="col-6 px-5 py-2 mb-3">
                    <form @submit.prevent>
                        <base-input
                            labelText="Количество препарат, мг"
                            inputType="number"
                            inputPlaceholder="Введите количество препарата:"
                            v-model="amount_drug"
                            class="mt-4 mb-4"
                        />
                        <base-input
                            labelText="Общий объем раствора, мл"
                            inputType="number"
                            inputPlaceholder="Введите общий объем раствора:"
                            v-model="volume"
                            class="mt-4 mb-4"
                        />
                        <base-input
                            labelText="Вес пациента, кг"
                            inputType="number"
                            inputPlaceholder="Введите вес пациента:"
                            v-model="weight_patient"
                            class="mt-4 mb-4"
                        />
                        <base-input
                            labelText="Дозировка в мкг*кг/мин или мл/час"
                            inputType="number"
                            inputPlaceholder="Введите дозировку:"
                            v-model="dosage"
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
                <div class="col-6 row my-auto h-50 w-50 border pb-3 bg-light bg-gradient">
                    <div class="col-12 my-auto border">
                        Результат вычисления: {{ result }} мл/час
                    </div>
                    <div class="col-12 border">
                        А это значит: {{ (parseFloat(result) * 20 / 60).toFixed(2) }} капель в минуту
                    </div>
                </div>
            </div>
        </div>

        <div class="content px-3">
            <div>
                <div>
                    <h2>Об калькуляторе</h2>
                    <p>
                       {{ calculatorInfo?.info.split('Формула:')[0] }}
                    </p>
                </div>
                <div>
                    <h2>Формула</h2>
                    <img
                        src="../../static/image/calculators/titration_rate/formula.png"
                        width=""
                        alt="Формула"
                        class="d-inline-block align-middle mr-2"
                    />
                    <p>
                        Скорость инфузии = масса тела пациента (кг) * доза препарата (мкг/кг*мин) /
                        (количество препарата в инфузионном растворе (мг) * (1 000/общий объем
                        инфузионного раствора))*60
                    </p>
                </div>
                <div>
                    <h2>Дополнительные сведения</h2>
                    <p>
                        Диапазон доз и начальные скорости введения некоторых распространенных
                        препаратов для пациента с массой тела 70 кг при разведении до общего объема
                        раствора равным 20 мл
                    </p>
                    <img
                    src="../../static/image/calculators/titration_rate/table.png"
                    width=""
                    alt="Таблица"
                    class="d-inline-block align-middle mr-2"
                />
                </div>
                <div class="content mt-3">
                    <h2>Краткие замечания по описанным препаратам</h2>
                    <h3>Дофамин</h3>
                    <p>
                        Если скорость инфузии > 20—30 мкг/кг/мин, дофамин целесообразно заменить
                        другим сосудосуживающим средством (адреналин, норадреналин). Действие на
                        гемодинамику зависит от дозы: Низкая доза: 1—5 мкг/кг/мин, увеличивает
                        почечный кровоток и диурез. Средняя доза: 5—15 мкг/кг/мин, увеличивает
                        почечный кровоток, ЧСС, сократимость миокарда и сердечный выброс. Высокая
                        доза: > 15 мкг/кг/мин, оказывает сосудосуживающее действие.
                    </p>
                    <h3>Фенилэфрин</h3>
                    <p>
                        Можно вводить болюсно по 25 - 100 мкг. Через несколько часов развивается
                        тахифилаксия.
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>
