from flask import Flask, render_template

app = Flask(__name__)

produtos = {
    1: {
        "id": 1,
        "nome": "O meu pé de laranja lima",
        "preco": "34,80",
        "imagem": "laranja.jpg",
        "autor": "José Mauro de Vasconcelos",
        "descricao": "Um clássico da literatura brasileira.",
        "detalhes": [
            "Editora: Melhoramentos",
            "Idioma: Português",
            "Páginas: 192"
        ],
        "categoria": "livros-nacionais",
        "ribbon": "Novo"
    },
    2: {
        "id": 2,
        "nome": "Hilda Furacão",
        "preco": "40,18",
        "imagem": "hilda.jpg",
        "autor": "Roberto Drummond",
        "descricao": "Romance ambientado em Belo Horizonte.",
        "detalhes": [
            "Editora: Companhia das Letras",
            "Idioma: Português",
            "Páginas: 304"
        ],
        "categoria": "livros-nacionais",
        "ribbon": "Promoção"
    }
}

@app.route("/")
def index():
    return "Home"

@app.route("/categoria/<nome>")
def categoria(nome):
    lista = [p for p in produtos.values() if p["categoria"] == nome]
    return render_template(
        "produtos/categoria.html",
        categoria={"nome": nome.replace("-", " ").title(), "produtos": lista}
    )

@app.route("/produto/<int:produto_id>")
def detalhe_produto(produto_id):
    produto = produtos.get(produto_id)
    if not produto:
        return "Produto não encontrado", 404
    return render_template("produtos/detalhe.html", produto=produto)

if __name__ == "__main__":
    app.run(debug=True)

