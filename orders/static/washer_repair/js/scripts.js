document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector(".burger");
    const headerMenu = document.querySelector(".header__menu");
    const modal = new bootstrap.Modal(document.getElementById("modal"));
    const dialog = document.getElementById("dialog");
    const toastElement = document.getElementById("toast");
    const toastBody = document.getElementById("toast-body");
    const toast = new bootstrap.Toast(toastElement, {delay: 15000});

    const toggleMenu = () => {
        burger.classList.toggle('active');
        headerMenu.classList.toggle("open");
    };

    const closeMenu = (event) => {
        if (!event.target.closest('.burger') && !event.target.closest('.header__menu') && headerMenu.classList.contains('open')) {
            toggleMenu();
        }
    };
    const handleKeyDown = (event) => {
        if (event.key === 'Escape' && headerMenu.classList.contains('open')) {
            toggleMenu();
        }
    };

    burger.addEventListener('click', toggleMenu);
    document.addEventListener('click', closeMenu);
    document.addEventListener('keydown', handleKeyDown);

    [...headerMenu.querySelectorAll('a, button')].forEach(element => {
        element.addEventListener('click', toggleMenu);
    });

    htmx.on("htmx:afterSwap", ({detail: {target}}) => {
        if (target.id === "dialog") modal.show();
    });

    htmx.on("htmx:beforeSwap", ({detail}) => {
        if (detail.target.id === "dialog" && !detail.xhr.response) {
            modal.hide();
            detail.shouldSwap = false;
        }
    });

    htmx.on("hidden.bs.modal", () => {
        dialog.innerHTML = "";
    });

    htmx.on("showMessage", ({detail: {value}}) => {
        toastBody.innerText = value;
        toast.show();
    });
});