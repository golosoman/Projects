<template>
    <div class="content">
        <div class="container mt-5 mb-5 d-flex justify-content-center">
            <div class="card rounded">
                <div class="d-block justify-content-center">
                    <div class="area1 p-3 py-5"></div>
                    <div class="area2 p- text-center px-3">
                        <div class="image mr-3">
                            <img
                                src="../static/image/author.png"
                                class="rounded-circle"
                                width="100"
                            />
                            <h4 class="name mt-3">Лапин Константин Сергеевич</h4>
                            <p class="information mt-3 text-justify">
                                Меня зовут Лапин Константин, и я студент третьего курса
                                специальности фундаментальная информатика и информационные
                                технологии (ФИИТ) Самарского университета.
                            </p>
                            <p class="information mt-3 text-justify">
                                Параллельно с учебой я углубленно изучаю языки программирования и
                                технологии разработки программного обеспечения. Я знаком с такими
                                языками, как Python, C#, Java, C/C++. Также я работал с базами
                                данных MySQL, SQLite3 и MongoDB. Кроме того, я знаком со средой для
                                разработки графических приложений: Unity
                            </p>
                            <p class="information mt-3 text-justify">
                                У меня есть практический опыт разработки веб-приложений как в 
                                backend-е, так и frontend-е. Я работал с Node.js, Express, Nest.js,
                                JavaScript, TypeScript, Vue, HTML и CSS.
                            </p>
                            <p class="information mt-3 text-justify">
                                Я уверен, что мои знания и навыки позволят мне стать успешным
                                специалистом в области информационных технологий. Я готов к новым
                                вызовам и задачам и стремлюсь к постоянному профессиональному росту.
                            </p>
                            <p class="information mt-3 text-justify">
                                Документацию к калькуляторам можете найти здесь: <a href="http://localhost:8080/swagger-ui/index.html#/Контроллер%20API%20калькуляторов/get">ТЫК</a>
                            </p>
                            <div class="d-flex justify-content-center mt-5">
                                <a class="btn btn-secondary mx-2" href="https://github.com/golosoman">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        fill="currentColor"
                                        class="bi bi-github"
                                        viewBox="0 0 16 16"
                                    >
                                        <path
                                            d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8"
                                        ></path>
                                    </svg>
                                </a>
                                <a class="btn btn-primary" href="https://t.me/Golosoman">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        fill="currentColor"
                                        class="bi bi-telegram"
                                        viewBox="0 0 16 16"
                                    >
                                        <path
                                            d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"
                                        />
                                    </svg>
                                </a>
                            </div>
                        </div>
                        <div></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.card {
    width: 500px;
    border: none;
    border-radius: 14px !important;
}
.area1 {
    background-color: #6f6f84;
    border-top-left-radius: 14px !important;
    border-top-right-radius: 14px !important;
    padding-top: 83px !important;
}
.image {
    top: -62px;
    position: relative;
}
.image img {
    box-shadow: 5px 6px 6px 2px #454d56;
}
.area2 {
    background-color: #fff;
    border-bottom-left-radius: 14px !important;
    border-bottom-right-radius: 14px !important;
}
.name {
    font-size: 25px;
    font-weight: 650;
}
.information {
    color: #737a9f;
    font-weight: 500;
    font-size: 16px;
}
@media (max-width: 700px) {
    .list-icons {
        display: block;
    }
}
</style>
