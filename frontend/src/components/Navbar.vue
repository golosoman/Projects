<template>
    <nav class="navbar navbar-expand-lg py-2 navbar-dark bg-dark shadow-sm">
        <div class="container">
            <a href="#" class="navbar-brand">
                <!-- Logo Image -->
                <img
                    src="../static/image/logo.png"
                    width="45"
                    alt=""
                    class="d-inline-block align-middle mr-2"
                />
                <!-- Logo Text -->
                <span class="font-weight-bold">Медицинские калькуляторы </span>
            </a>

            <button
                type="button"
                data-toggle="collapse"
                data-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation"
                class="navbar-toggler"
            >
                <span class="navbar-toggler-icon"></span>
            </button>

            <div id="navbarSupportedContent" class="collapse navbar-collapse">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item active">
                        <a href="/" class="nav-link"
                            >Главная <span class="sr-only">(current)</span></a
                        >
                    </li>
                    <li class="nav-item"><a href="/about" class="nav-link">Автор</a></li>
                    <li class="nav-item dropdown">
                        <a
                            class="nav-link dropdown-toggle"
                            href="#"
                            id="navbarDropdown"
                            role="button"
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false"
                        >
                            Калькуляторы
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                            <li>
                                <a class="dropdown-item" href="/calculator/body-mass-index"
                                    >Расчет Индекса массы тела</a
                                >
                            </li>
                            <li>
                                <a class="dropdown-item" href="/calculator/titration-rate"
                                    >Расчет скорости титрования</a
                                >
                            </li>
                            <li>
                                <a
                                    class="dropdown-item"
                                    href="/calculator/rate-intravenous-drip-drug"
                                    >Расчет скорости внутривенного капельного введения препарата</a
                                >
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
<script>
import 'https://code.jquery.com/jquery-3.5.1.slim.min.js'
import 'https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js'
</script>
