$(document).ready(function () {
    // Плавный скроллинг к якорным ссылкам
    $('a[href^="#"]').on('click', function (event) {
        let target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top
            }, 1000); // Продолжительность анимации в миллисекундах
        }
    });
});