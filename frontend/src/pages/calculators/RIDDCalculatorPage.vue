<script lang="ts">
import {ref} from 'vue'
export default {
    setup(props, ctx) {
        let volume = ref('');
        let time = ref('');

        return {
            volume, time
        }
    },
}
</script>
<template>
    <div class="content">
        <h1>Калькулятор для расчет скорости внутривенного капельного введения препарата</h1>
        <div>
            <form @submit.prevent>
                <base-input 
                    labelText="Объем раствора, мл"
                    inputType="number"
                    inputPlaceholder="Введите объем раствора:"
                    v-model="volume"
                    class="mt-4  mb-4"
                />
                <base-input 
                    labelText="Желаемое время введения, часов"
                    inputType="number"
                    inputPlaceholder="Введите желаемое время введения:"
                    v-model="time"
                    class="mt-4  mb-4"
                />
                <base-button>Рассчитать</base-button>
                <base-button>Сбросить</base-button>
            </form>
        </div>
        
            
        <div>
            <div>
                <h2>
                    Об калькуляторе
                </h2>
                <p>
                    *Расчет скорости внутривенного капельного введения препарата
                </p>
            </div>
           <div>
                <h2>
                    Формула
                </h2>
                <p>
                    Расчет производится по следующей формуле:

                    количество капель в минуту = V*20/t,

                    где V - объем раствора в милилитрах, t - время в минутах, 20 - среднее количество капель в милилитре, v - скорость введения в каплях в минуту
                </p>
           </div>
        </div>
    </div>
</template>
