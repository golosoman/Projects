<template>
    <div data-mdb-input-init class="form-outline">
        <label class="form-label" :for="id">{{ labelText }}</label>
        <input
            :value="modelValue"
            @input="updateInput"
            class="form-control"
            :id="id"
            :type="inputType"
            :placeholder="inputPlaceholder"
        />
    </div>
</template>

<script lang="ts">
import { onMounted, ref } from 'vue'
export default {
    name: 'base-input',
    props: {
        modelValue: {
            type: [String, Number],
            required: true,
            default: ''
        },
        labelText: {
            type: [String, Number],
            required: true,
            default: 'Поле ввода'
        },
        inputPlaceholder: {
            type: String,
            required: true,
            default: 'Ввод: '
        },
        inputType: {
            type: String,
            required: true,
            default: 'text'
        }
    },
    setup() {
        let id = ref('')

        const setUniqId = () => {
            const date = new Date()
            const timestamp = date.getTime()
            const randomString = Math.random().toString(36).substring(7)
            const randomNumber = Math.floor(Math.random() * 10000)
            const uniqueId = `id-${timestamp}-${randomString}-${randomNumber}`
            return uniqueId
        }

        onMounted(() => {
            id.value = setUniqId()
        })

        return { id }
    },
    methods: {
        updateInput(event) {
            this.$emit('update:modelValue', event.target.value)
        }
    }
}
</script>

<style scoped></style>
