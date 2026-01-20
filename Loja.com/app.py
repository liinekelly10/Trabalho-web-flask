from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/categoria/<nome>")
def categoria(nome):
    lista = [p for p in produtos if p["categoria"] == nome]
    return render_template(
        "Categorias/categoria.html",
        categoria={
            "nome": nome.replace("-", " ").title(),
            "produtos": lista
        }
    )

@app.route("/produto/<int:produto_id>")
def detalhe_produto(produto_id):
    produto = produtos.get(produto_id)
    if not produto:
        return "Produto não encontrado", 404
    return render_template("produtos/detalhe.html", produto=produto)

@app.route("/carrinho")
def carrinho():
    return render_template("Carrinho/carrinho.html")

produtos = [
    # ===== NACIONAIS =====
    {
        "id": 1,
        "nome": "O meu pé de laranja lima",
        "preco": "34,80",
        "imagem": "laranja.jpg",
        "categoria": "livros-nacionais",
        "ribbon": "Novo"
    },
    {
        "id": 2,
        "nome": "Hilda Furacão",
        "preco": "40,18",
        "imagem": "hilda.jpg",
        "categoria": "livros-nacionais",
        "ribbon": "Promoção"
    },
    {
        "id": 3,
        "nome": "Bom dia, Verônica",
        "preco": "49,90",
        "imagem": "bomdia.jpg",
        "categoria": "livros-nacionais",
        "ribbon": "Top 2"
    },
    {
        "id": 4,
        "nome": "A cabeça do santo",
        "preco": "39,90",
        "imagem": "santo.jpg",
        "categoria": "livros-nacionais",
        "ribbon": "Novo"
    },

    # ===== CLÁSSICOS =====
    {
        "id": 5,
        "nome": "Crime e Castigo",
        "preco": "25,90",
        "imagem": "crime-castigo.jpg",
        "categoria": "classicos",
        "ribbon": "Top 3"
    },
    {
        "id": 6,
        "nome": "A Metamorfose",
        "preco": "22,90",
        "imagem": "metamorfose.jpg",
        "categoria": "classicos",
        "ribbon": "Promoção"
    },
    {
        "id": 7,
        "nome": "Dom Casmurro",
        "preco": "29,90",
        "imagem": "casmurro.jpg",
        "categoria": "classicos",
        "ribbon": "Top 5"
    },
    {
        "id": 8,
        "nome": "O Alienista",
        "preco": "26,62",
        "imagem": "alienista.jpg",
        "categoria": "classicos",
        "ribbon": "Novo"
    },

    # ===== INFANTOJUVENIL =====
    {
        "id": 9,
        "nome": "Turma da Mônica Jovem nº 50",
        "preco": "19,60",
        "imagem": "monica.jpg",
        "categoria": "infantojuvenil",
        "ribbon": "Novo"
    },
    {
        "id": 10,
        "nome": "O menino, a toupeira, a raposa e o cavalo",
        "preco": "71,15",
        "imagem": "toupeira.jpg",
        "categoria": "infantojuvenil",
        "ribbon": "Promoção"
    },
    {
        "id": 11,
        "nome": "O Pequeno Príncipe",
        "preco": "8,55",
        "imagem": "oprincipe.jpg",
        "categoria": "infantojuvenil",
        "ribbon": "Top 4"
    },
    {
        "id": 12,
        "nome": "O Mágico de Oz",
        "preco": "39,00",
        "imagem": "oz.jpg",
        "categoria": "infantojuvenil",
        "ribbon": "Novo"
    },

    # ===== TERROR =====
    {
        "id": 13,
        "nome": "Carrie – Coleção",
        "preco": "99,90",
        "imagem": "carrie.jpg",
        "categoria": "terror",
        "ribbon": "Novo"
    },
    {
        "id": 14,
        "nome": "Ed e Lorraine Warren",
        "preco": "55,89",
        "imagem": "warren.jpg",
        "categoria": "terror",
        "ribbon": "Promoção"
    },
    {
        "id": 15,
        "nome": "O Vilarejo",
        "preco": "39,90",
        "imagem": "vilarejo.jpg",
        "categoria": "terror",
        "ribbon": "Top 1"
    },
    {
        "id": 16,
        "nome": "It – A Coisa",
        "preco": "46,90",
        "imagem": "it.jpg",
        "categoria": "terror",
        "ribbon": "Novo"
    }
]

if __name__ == "__main__":
    app.run(debug=True)

