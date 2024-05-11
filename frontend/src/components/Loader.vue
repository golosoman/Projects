<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="loader"></div>
</template>

<style scoped>
.loader {
    width: 88px;
    height: 88px;

    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    display: inline-block;
    border: 2px solid #000000;
    box-sizing: border-box;
    animation: rotation 2s linear infinite;
}
.loader::after,
.loader::before {
    content: '';
    box-sizing: border-box;
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    margin: auto;
    border: 2px solid #3cbeee;
    width: 68px;
    height: 68px;
    animation: rotationBack 1.5s linear infinite;
    transform-origin: center center;
}
.loader::before {
    width: 48px;
    height: 48px;
    border-color: #322f2f;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
}

@keyframes rotation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
@keyframes rotationBack {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(-360deg);
    }
}
</style>
