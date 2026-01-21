document.addEventListener("DOMContentLoaded", () => {
    const finishBtn = document.getElementById("finishPurchase");
    const clearBtn = document.getElementById("clearCartBtn");
    const toastContainer = document.getElementById("toastContainer");

    // Função para criar toast
    function showToast(message, type = "success") {
        const toast = document.createElement("div");
        toast.classList.add("toast", type);
        toast.textContent = message;
        toastContainer.appendChild(toast);

        // Remove o toast depois de 3 segundos
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // Finalizar Compra
    if (finishBtn) {
        finishBtn.addEventListener("click", async () => {
            const items = document.querySelectorAll(".cart-table tbody tr");

            if (items.length === 0) {
                showToast("Seu carrinho está vazio.", "error");
                return;
            }

            try {
                const response = await fetch("/api/carrinho/finalizar", { method: "POST" });
                const data = await response.json();

                if (response.ok) {
                    showToast(data.sucesso, "success");

                    // Limpa tabela do carrinho no front-end
                    const tbody = document.querySelector(".cart-table tbody");
                    if (tbody) tbody.innerHTML = "";
                    const total = document.querySelector(".cart-grand-total");
                    if (total) total.textContent = "Total: R$ 0.00";
                } else {
                    showToast(data.erro, "error");
                }
            } catch (err) {
                showToast("Erro ao finalizar a compra.", "error");
            }
        });
    }

    // Esvaziar Carrinho
    if (clearBtn) {
        clearBtn.addEventListener("click", async () => {
            try {
                const response = await fetch("/api/carrinho/finalizar", { method: "POST" });
                const data = await response.json();

                if (response.ok) {
                    showToast("Carrinho esvaziado.", "success");

                    // Limpa tabela do carrinho no front-end
                    const tbody = document.querySelector(".cart-table tbody");
                    if (tbody) tbody.innerHTML = "";
                    const total = document.querySelector(".cart-grand-total");
                    if (total) total.textContent = "Total: R$ 0.00";
                } else {
                    showToast(data.erro, "error");
                }
            } catch {
                showToast("Erro ao esvaziar o carrinho.", "error");
            }
        });
    }
});
