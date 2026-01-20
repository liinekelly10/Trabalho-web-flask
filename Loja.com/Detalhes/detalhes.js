function addToCart() {
    const card = document.querySelector(".product-card");

    if (!card) {
        console.error("ERRO: .product-card não encontrado.");
        return;
    }

    // pegar dados do produto
    const id = card.dataset.id;
    const name = card.dataset.name;
    const price = parseFloat(card.dataset.price);
    const image = card.dataset.image;

    if (!id || !name || isNaN(price)) {
        alert("Erro: Dados do produto estão incompletos.");
        console.log("Dados lidos:", card.dataset);
        return;
    }

    const newItem = {
        id,
        name,
        price,
        image,
        qty: 1
    };

    // carregar carrinho
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    // verificar se já existe
    let item = cart.find(p => p.id === id);

    if (item) {
        item.qty++;
    } else {
        cart.push(newItem);
    }

    // salvar
    localStorage.setItem("cart", JSON.stringify(cart));

    alert(`${name} foi adicionado ao carrinho!`);
    console.log("Carrinho após adicionar:", cart);
}
