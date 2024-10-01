<template>
    <a data-mdb-ripple-init href="#!">
        <img
            :alt="altContent"
            class="img-fluid rounded"
            :src="staticPath + srcContent"
        />
    </a>
</template>

<script>
export default {
    name: 'base-image',
    props: {
        altContent: {
            type: String,
            required: true,
            default: 'Здесь должна быть какая-то картинка'
        },
        srcContent: {
            type: String,
            required: true
        },
        staticPath: {
            type: String,
            required: true,
            default: 'http://localhost:5000/'
        }
    }
}
</script>
