// ---------------------------
//  CARREGAMENTO INICIAL
// ---------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadCartFromStorage();
    updateTotals();
    setupFinishButton();
    setupClearCartButton(); // << BOTÃO PARA ESVAZIAR O CARRINHO
});

// ---------------------------
//  EVENTOS DE AUMENTAR / DIMINUIR
// ---------------------------
document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("tbody");
    if (!tableBody) return;

    tableBody.addEventListener("click", (e) => {
        const btn = e.target.closest(".btn-qtd");
        if (!btn) return;

        const isIncrease = btn.classList.contains("increase");
        const isDecrease = btn.classList.contains("decrease");
        if (!isIncrease && !isDecrease) return;

        const tr = btn.closest("tr");
        const td = btn.closest(".qtd");
        const input = td.querySelector(".input-qtd");

        const price = parseFloat(tr.dataset.price) || 0;
        let qty = parseInt(input.value, 10) || 0;

        qty = isIncrease ? qty + 1 : qty - 1;

        // remover item se zerar
        if (qty <= 0) {
            const confirmed = confirm("Quantidade zerada. Deseja remover este item do carrinho?");
            if (confirmed) {
                tr.remove();
                updateTotals();
                saveCartToStorage();
            } else {
                input.value = 1;
                updateTotals();
            }
            return;
        }

        // atualiza quantidade
        input.value = qty;

        // atualiza total do item
        const itemTotalCell = tr.querySelector(".item-total");
        if (itemTotalCell) {
            itemTotalCell.textContent = formatBRL(price * qty);
        }

        updateTotals();
        saveCartToStorage();
    });
});

// ---------------------------
//  ATUALIZA TOTAIS
// ---------------------------
function updateTotals() {
    const rows = document.querySelectorAll("tbody tr");
    let grand = 0;

    rows.forEach(row => {
        const price = parseFloat(row.dataset.price) || 0;
        const input = row.querySelector(".input-qtd");
        const qty = input ? (parseInt(input.value, 10) || 0) : 0;
        const itemTotalCell = row.querySelector(".item-total");

        const itemTotal = price * qty;
        if (itemTotalCell) itemTotalCell.textContent = formatBRL(itemTotal);

        grand += itemTotal;
    });

    let totalBox = document.querySelector(".cart-grand-total");
    if (!totalBox) {
        totalBox = document.createElement("div");
        totalBox.className = "cart-grand-total";
        totalBox.style.marginTop = "18px";
        totalBox.style.fontWeight = "700";
        totalBox.style.fontSize = "18px";
        totalBox.style.textAlign = "right";
        const container = document.querySelector(".container");
        container.appendChild(totalBox);
    }

    totalBox.textContent = "Total: " + formatBRL(grand);
}

// ---------------------------
//  FORMATAÇÃO BRL
// ---------------------------
function formatBRL(number) {
    return "R$ " + Number(number).toFixed(2).replace(".", ",");
}

// ---------------------------
//  CARREGA DO STORAGE
// ---------------------------
function loadCartFromStorage() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const tbody = document.querySelector("tbody");
    tbody.innerHTML = "";

    cart.forEach(item => {
        const tr = document.createElement("tr");
        tr.dataset.price = item.price;

        tr.innerHTML = `
            <td><img src="${item.image}" class="cart-img"></td>

            <td class="desc">
                ${item.name}<br>
            </td>

            <td class="qtd">
                <button class="btn-qtd decrease">–</button>
                <input type="number" value="${item.qty}" min="1" class="input-qtd" readonly>
                <button class="btn-qtd increase">+</button>
            </td>

            <td class="item-total">${formatBRL(item.price * item.qty)}</td>
        `;

        tbody.appendChild(tr);
    });
}

// ---------------------------
//  SALVA NO STORAGE
// ---------------------------
function saveCartToStorage() {
    const rows = document.querySelectorAll("tbody tr");
    const cart = [];

    rows.forEach(row => {
        const name = row.querySelector(".desc").innerText.trim();
        const image = row.querySelector(".cart-img").src;
        const price = parseFloat(row.dataset.price);
        const qty = parseInt(row.querySelector(".input-qtd").value, 10);

        cart.push({ name, image, price, qty });
    });

    localStorage.setItem("cart", JSON.stringify(cart));
}

// ---------------------------
//  FINALIZAR COMPRA
// ---------------------------
function setupFinishButton() {
    const btnFinish = document.querySelector(".finish-btn");
    if (!btnFinish) return;

    btnFinish.addEventListener("click", () => {
        alert("Compra realizada com sucesso!");

        // limpa tabela
        document.querySelector("tbody").innerHTML = "";

        // limpa storage
        localStorage.removeItem("cart");

        updateTotals();
    });
}

// ---------------------------
//  ESVAZIAR CARRINHO (NOVO)
// ---------------------------
function setupClearCartButton() {
    const btnClear = document.querySelector(".clear-cart-btn");
    if (!btnClear) return;

    btnClear.addEventListener("click", () => {
        const ok = confirm("Deseja realmente esvaziar o carrinho?");
        if (!ok) return;

        document.querySelector("tbody").innerHTML = "";
        localStorage.removeItem("cart");
        updateTotals();
    });
}
