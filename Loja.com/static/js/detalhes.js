document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form[action*='add-carrinho']");

    if (!form) return;

    form.addEventListener("submit", () => {
        // UX opcional
        console.log("Produto enviado para o backend (Flask)");
    });
});
