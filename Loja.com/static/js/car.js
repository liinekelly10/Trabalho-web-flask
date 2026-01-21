document.addEventListener("DOMContentLoaded", () => {
    const finishBtn = document.getElementById("finishPurchase");
    const alertBox = document.getElementById("alertBox");

    if (!finishBtn) return;

    finishBtn.addEventListener("click", () => {
        const items = document.querySelectorAll(".cart-table tbody tr");

        // 🔴 Carrinho vazio
        if (items.length === 0) {
            showMessage("Seu carrinho está vazio.", "error");
            return;
        }

        // ✅ Compra realizada
        showMessage("Compra realizada com sucesso!", "success");

        // ⏳ Simula finalização e limpa carrinho
        setTimeout(() => {
            window.location.href = "/carrinho/limpar";
        }, 2000);
    });

    function showMessage(text, type) {
        alertBox.textContent = text;
        alertBox.className = `alert ${type}`;
        alertBox.classList.remove("hidden");
    }
});
