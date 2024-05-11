<template>
    <button data-mdb-ripple-init class="btn btn-dark btn-block">
        <slot></slot>
    </button>
</template>
<script>
import { Ripple, initMDB } from 'mdb-ui-kit'
export default {
    name: 'base-button',
    setup() {
        initMDB({ Ripple })
    }
}
</script>
<style scoped></style>
