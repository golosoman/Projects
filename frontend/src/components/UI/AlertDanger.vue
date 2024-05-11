<template>
  <div v-if="visible" class="alert alert-danger alert-dismissible fade show position-fixed w-100" role="alert">
    <p><i>{{ `Произошла ошибка! ` }}</i> <b>{{ message }}</b></p>
    <button type="button" class="btn-close" @click="closeNotification"></button>
  </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  name: 'alert-danger',
  props: {
    message: {
      type: String,
      default: 'Ошибка!'
    },
    duration: {
      type: Number,
      default: 5000 // 5 секунд
    }
  },
  emits: ['editMessage'],
  setup(props, {emit}) {
    let visible = ref(false);
    let timeoutId = ref(null);
    // Отобразить уведомление при обновлении сообщения об ошибке
    watch(() => props.message, () => {
      // Проверяем, пустое ли сообщение
      if (!props.message.trim()) return;

      visible.value = true;

      // Отменяем предыдущий таймаут, если он есть
      if (timeoutId.value) {
        clearTimeout(timeoutId.value)
      };

      // Скрыть уведомление через указанный интервал времени
      timeoutId.value = setTimeout(() => {
        visible.value = false;
        emit('editMessage')
      }, props.duration);
    });

    const closeNotification = () => {
      visible.value = false;
      emit('editMessage')
    };

    return {
      visible,
      timeoutId,
      closeNotification
    };
  }
}
</script>