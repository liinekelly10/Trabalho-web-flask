from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from models import db, Usuario

app = Flask(__name__)
app.secret_key = "chave-secreta-loja"

# ---------------------------
# CONFIG BANCO
# ---------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loja.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------------------
# HOME
# ---------------------------

@app.route("/")
def index():
    return render_template("index.html")
# ---------------------------
# CADASTRO
# ---------------------------
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        # Verifica se veio JSON
        if request.is_json:
            dados = request.get_json()
            nome = dados.get("nome")
            username = dados.get("username")  # <- pega o username
            email = dados.get("email")
            senha = dados.get("senha")
        else:
            # Formulário tradicional
            nome = request.form.get("Nome_C")
            email = request.form.get("email")
            senha = request.form.get("pass")

        # verifica se email já existe
        if Usuario.query.filter_by(email=email).first():
            if request.is_json:
                return jsonify({"erro": "E-mail já cadastrado"}), 400
            return render_template(
                "Cadastro/cadastro.html",
                erro="E-mail já cadastrado"
            )

        usuario = Usuario(nome=nome, email=email)
        usuario.set_senha(senha)

        db.session.add(usuario)
        db.session.commit()

        if request.is_json:
            return jsonify({"sucesso": "Usuário cadastrado"}), 201

        return redirect(url_for("login"))

    return render_template("Cadastro/cadastro.html")


@app.route("/api/cadastro", methods=["POST"])
def api_cadastro():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    nome = dados.get("nome")
    username = dados.get("username")
    email = dados.get("email")
    senha = dados.get("senha")

    if not all([nome, username, email, senha]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "E-mail já cadastrado"}), 400

    if Usuario.query.filter_by(username=username).first():
        return jsonify({"erro": "Username já cadastrado"}), 400

    usuario = Usuario(nome=nome, username=username, email=email)
    usuario.set_senha(senha)

    db.session.add(usuario)
    db.session.commit()

    return jsonify({"sucesso": "Usuário cadastrado", "usuario": usuario.to_dict()}), 201


# ---------------------------
# LOGIN
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("password")

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.verificar_senha(senha):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            return redirect(url_for("carrinho"))

        return render_template(
            "Login/login.html",
            erro="E-mail ou senha inválidos"
        )

    return render_template("Login/login.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    email = dados.get("email")
    senha = dados.get("senha")

    if not all([email, senha]):
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"erro": "E-mail ou senha inválidos"}), 401

    # Podemos usar um token fake ou JWT (simplificado aqui)
    session["usuario_id"] = usuario.id

    return jsonify({"sucesso": "Login realizado", "usuario": usuario.to_dict()}), 200


# ---------------------------
# LOGOUT
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ---------------------------
# CATEGORIA
# ---------------------------

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

@app.route("/api/categorias/<string:nome>", methods=["GET"])
def api_categoria(nome):
    lista = [p for p in produtos if p["categoria"] == nome]
    return jsonify({"categoria": nome, "produtos": lista}), 200

@app.route("/api/produtos/categoria/<string:categoria>", methods=["GET"])
def api_produtos_por_categoria(categoria):
    # Filtra produtos pela categoria (comparando string)
    produtos_filtrados = [p for p in produtos if p.get("categoria") == categoria]

    if not produtos_filtrados:
        return jsonify({"erro": f"Nenhum produto encontrado para a categoria '{categoria}'"}), 404

    # Retorna apenas os campos essenciais
    resultado = []
    for p in produtos_filtrados:
        resultado.append({
            "id": p["id"],
            "nome": p["nome"],
            "preco": p["preco"],
            "imagem": p["imagem"],
            "categoria": p["categoria"]
        })

    return jsonify(resultado), 200


# ---------------------------
# DETALHE DO PRODUTO
# ---------------------------

@app.route("/produto/<int:produto_id>")
def detalhe_produto(produto_id):
    produto = next((p for p in produtos if p["id"] == produto_id), None)

    if not produto:
        return "Produto não encontrado", 404

    return render_template(
        "Detalhes/detalhes.html",
        produto=produto
    )

@app.route("/api/produtos", methods=["GET"])
def api_produtos():
    return jsonify(produtos), 200

@app.route("/api/produtos/<int:produto_id>", methods=["GET"])
def api_produto(produto_id):
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # Reorganiza os campos: coloca 'id' primeiro
    produto_reordenado = {
        "id": produto["id"],
        "nome": produto["nome"],
        "autor": produto["autor"],
        "categoria": produto["categoria"],
        "preco": produto["preco"],
        "imagem": produto["imagem"],
        "ribbon": produto.get("ribbon"),
        "descricao": produto["descricao"],
        "detalhes": produto["detalhes"],
        "detalhes_compra": produto["detalhes_compra"]
    }

    return jsonify(produto_reordenado), 200

@app.route("/api/usuarios", methods=["GET"])
def api_usuarios():
    usuarios = Usuario.query.all()
    lista = []

    for u in usuarios:
        lista.append({
            "id": u.id,
            "nome": u.nome,
            "username": getattr(u, "username", None),  # caso tenha username
            "email": u.email
        })

    return jsonify(lista), 200

# ---------------------------
# CARRINHO
# ---------------------------
@app.route("/carrinho")
def carrinho():
    cart = session.get("cart", [])

    total = sum(item["preco"] * item["qty"] for item in cart)

    return render_template(
        "Carrinho/carrinho.html",
        cart=cart,
        total=total
    )

@app.route("/api/carrinho", methods=["GET", "POST"])
def api_carrinho():
    if request.method == "POST":
        dados = request.get_json()
        produto_id = dados.get("produto_id")
        qty = dados.get("qty", 1)
        
        produto = next((p for p in produtos if p["id"] == produto_id), None)
        if not produto:
            return jsonify({"erro": "Produto não encontrado"}), 404

        cart = session.get("cart", [])
        for item in cart:
            if item["id"] == produto_id:
                item["qty"] += qty
                session["cart"] = cart
                return jsonify(cart), 200

        cart.append({
            "id": produto["id"],
            "nome": produto["nome"],
            "preco": float(produto["preco"].replace(",", ".")),
            "imagem": produto["imagem"],
            "qty": qty
        })
        session["cart"] = cart
        return jsonify(cart), 201

    # GET retorna o carrinho
    return jsonify(session.get("cart", [])), 200


# ---------------------------
# ADICIONAR AO CARRINHO
# ---------------------------
@app.route("/add-carrinho/<int:produto_id>", methods=["POST"])
def add_carrinho(produto_id):
    produto = next((p for p in produtos if p["id"] == produto_id), None)

    if not produto:
        return "Produto não encontrado", 404

    cart = session.get("cart", [])

    preco_float = float(produto["preco"].replace(",", "."))

    for item in cart:
        if item["id"] == produto_id:
            item["qty"] += 1
            session["cart"] = cart
            return redirect(url_for("carrinho"))

    cart.append({
        "id": produto["id"],
        "nome": produto["nome"],
        "preco": preco_float,
        "imagem": produto["imagem"],
        "qty": 1
    })

    session["cart"] = cart
    return redirect(url_for("carrinho"))

# ---------------------------
# AUMENTAR ITEM
# ---------------------------
@app.route("/carrinho/aumentar/<int:produto_id>")
def aumentar_item(produto_id):
    cart = session.get("cart", [])

    for item in cart:
        if item["id"] == produto_id:
            item["qty"] += 1
            break

    session["cart"] = cart
    return redirect(url_for("carrinho"))

# ---------------------------
# DIMINUIR ITEM
# ---------------------------
@app.route("/carrinho/diminuir/<int:produto_id>")
def diminuir_item(produto_id):
    cart = session.get("cart", [])

    for item in cart:
        if item["id"] == produto_id:
            item["qty"] -= 1
            if item["qty"] <= 0:
                cart.remove(item)
            break

    session["cart"] = cart
    return redirect(url_for("carrinho"))

# ---------------------------
# LIMPAR CARRINHO
# ---------------------------
@app.route("/carrinho/limpar")
def limpar_carrinho():
    session.pop("cart", None)
    return redirect(url_for("carrinho"))

@app.route("/api/carrinho/finalizar", methods=["POST"])
def finalizar_compra():
    cart = session.get("cart", [])

    if not cart or len(cart) == 0:
        return jsonify({"erro": "Carrinho vazio"}), 400

    # Aqui você poderia salvar a compra no banco, gerar pedido, etc.
    # Por enquanto, vamos apenas limpar o carrinho
    session.pop("cart", None)

    return jsonify({"sucesso": "Compra realizada com sucesso!"}), 200

produtos = [
    # ===== NACIONAIS =====
    {
        "id": 1,
        "nome": "O meu pé de laranja lima",
        "autor": "José Mauro de Vasconcelos",
        "preco": "34,80",
        "imagem": "laranja.jpg",
        "categoria": "livros-nacionais",
        "ribbon": "Novo",
        "descricao": (
            "O Meu Pé de Laranja Lima é desses livros que marcam época. Lançado em 1968, trata-se de uma "
            "história fortemente autobiográfica, que demonstra a mão de um escritor experiente, ciente do "
            "efeito que pode provocar nos leitores com suas cenas e a composição de seus personagens. "
            "O protagonista Zezé tem 6 anos e mora num bairro modesto, na zona norte do Rio de Janeiro. "
            "O pai está desempregado, e a família passa por dificuldades. O menino vive aprontando,"
            "sem jamais se conformar com as limitações que o mundo lhe impõe – viaja com sua imaginação, "
            "brinca, explora, descobre, responde aos adultos, mete-se em confusões, causa pequenos desastres. "
            "As surras que lhe aplicam seu pai e sua irmã mais velha são seu suplício, a ponto de fazê-lo "
            "querer desistir da vida. No entanto, o apego ao mundo que criou felizmente sempre fala mais alto. "
            "Só não há remédio para a dor, para a perda. E Zezé muito cedo descobrirá isso. A alegria e a "
            "tristeza não poderiam estar mais bem combinadas do que nestas páginas. E isso, se não explica, "
            "justifica a imensa popularidade alcançada pelo livro."
        ),
        "detalhes": [
            "Editora: Melhoramentos",
            "Data da Publicação: 1 maio 2019",
            "Edição: 1ª",
            "Idioma: Português",
            "Número de páginas: 232 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },

    {
        "id": 2,
        "nome": "Hilda Furacão",
        "autor": "Roberto Drummond",
        "preco": "40,18",
        "imagem": "hilda.jpg",
        "categoria": "livros-nacionais",
        "ribbon": "Promoção",
        "descricao": (
            "Hilda Furacão passa-se em Belo Horizonte no início dos anos 60, Hilda, "
            "a Garota do Maiô Dourado, enfeitiçava os homens na beira da piscina em um "
            "dos mais tradicionais clubes, o Minas Tênis. Por algum motivo secreto "
            "muda-se para o quarto 304 do Maravilhoso Hotel, na zona boêmia da cidade. "
            "Transformada em Hilda Furacão, a musa erótica tira o sono da cidade. "
            "Sua vida de fada sexual cruza-se com os sonhos de três rapazes vindos "
            "do interior: um é inspirado no notório Frei Betto, que queria ser santo, "
            "mas se tornaria frade franciscano, líder político e escritor. "
            "Outro queria ser ator em Hollywood ― torna-se dom Juan de aluguel. "
            "O terceiro, aquele que queria ter sua Sierra Maestra, é o próprio Roberto, "
            "narrador da história. Hilda Furacão é o desafio que o santo tem que enfrentar. "
            "O romance foi transformado em minissérie de grande sucesso pela TV Globo, "
            "com Ana Paula Arósio no papel de Hilda."
        ),
        "detalhes": [
            "Editora: Geração Editorial",
            "Data da Publicação: 1 abril 2008",
            "Edição: 3ª",
            "Idioma: Português",
            "Número de páginas: 296 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },
    {
        "id": 3,
        "nome": "Bom dia, Verônica",
        "autor": "Raphael Montes e Ilana Casoy",
        "preco": "49,90",
        "imagem": "bomdia.jpg",
        "categoria": "livros-nacionais",
        "ribbon": "Top 2",
        "descricao": (
            "Verônica Torres trabalha no Departamento de Homicídios e de Proteção à Pessoa, da Polícia Civil "
            "em São Paulo. É secretária de Carvana, um delegado pouco confiável, e filha de um respeitado "
            "policial, que teve um fim trágico e não totalmente esclarecido. Verônica está afastada de "
            "qualquer tipo de investigação, mas, ao presenciar o suicídio de uma mulher em seu trabalho, "
            "a fragilidade da vítima e as estranhas circunstâncias que a levaram à delegacia a colocam na "
            "trilha de um abusador com requintes de crueldade. Quando recebe uma ligação anônima de uma "
            "mulher desesperada, ela seguirá as pistas de uma série de crimes ainda mais sombrios. "
            "Janete é uma dona de casa devotada, que obedece Brandão, seu marido, pelo absoluto terror "
            "que nutre por ele. Policial militar, ele está acima do bem e do mal e pratica crimes "
            "sexuais de extrema violência e sadismo, em que ela é obrigada a participar ― primeiro, "
            "aliciando mulheres; depois, acompanhando o desenrolar de suas mortes. As vidas de "
            "Verônica e Janete se entrecruzam e as levam aos limites da violência e da loucura. "
            "Ao narrar suas histórias, Ilana Casoy e Raphael Montes criam um thriller sem paralelos "
            "na literatura policial brasileira, com uma trama complexa ― e uma investigadora inesquecível."
        ),
        "detalhes": [
            "Editora: Companhia das letras",
            "Data da Publicação: 22 agosto 2022",
            "Edição: 1ª",
            "Idioma: Português",
            "Número de páginas: 320 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },
    
    {
        "id": 4,
        "nome": "A cabeça do santo",
        "autor": "Socorro Aciolli",
        "preco": "39,90",
        "imagem": "santo.jpg",
        "categoria": "livros-nacionais",
        "ribbon": "Novo",
        "descricao": (
            "Pouco antes de morrer, a mãe de Samuel lhe faz um último pedido: que ele vá encontrar a avó "
            "e o pai que nunca conheceu. Mesmo contrariado, o rapaz cumpre a promessa e faz a pé o caminho "
            "de Juazeiro do Norte até a pequena cidade de Candeia, sofrendo todas as agruras do sol "
            "impiedoso do sertão do Ceará. Ao chegar àquela cidade quase fantasma, ele encontra abrigo "
            "num lugar curioso: a cabeça oca e gigantesca de uma estátua inacabada de santo Antônio, que "
            "jazia separada do resto do corpo. Mas as estranhezas não param aí: Samuel começa a escutar uma "
            "confusão de vozes femininas apenas quando está dentro da cabeça. Assustado, se dá conta de que "
            "aquilo são as preces que as mulheres fazem ao santo falando de amor. Seu primeiro contato na "
            "cidade será com Francisco, um rapaz de quem logo fica amigo e que resolve ajudá-lo a explorar "
            "comercialmente o seu dom da escuta, promovendo casamentos e outras artimanhas amorosas. "
            "Antes parada no tempo, a cidade aos poucos volta à vida, à medida que vai sendo tomada por "
            "fiéis de todos os cantos, atraídos pelo poder inaudito de Samuel. Em meio a esse tumulto, "
            "ele ainda irá se apaixonar por uma voz misteriosa que se destaca entre as tantas outras que "
            "ecoam na cabeça do santo. Já consagrada por seus livros infantojuvenis, a escritora Socorro "
            "Acioli apresenta este seu primeiro romance dirigido ao público adulto, desenvolvido na oficina "
            "Como Contar um Conto, promovida por Gabriel García Márquez em Cuba."
        ),
        "detalhes": [
            "Editora: Companhia das letras",
            "Data da Publicação: 7 de fevereiro 2014",
            "Edição: 1ª",
            "Idioma: Português",
            "Número de páginas: 176 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },

    # ===== INFANTOJUVENIL =====
    {
        "id": 5,
        "nome": "Turma da Mônica Jovem nº 50",
        "autor": "Mauricio de Sousa",
        "preco": "19,60",
        "imagem": "monica.jpg",
        "categoria": "infantojuvenil",
        "ribbon": "Novo",
        "descricao": (
            "Mais uma história cheia de humor e muitas emoções! Você está convidado" 
            "a assistir ao Casamento do Século: Mônica e Cebola se casam e você acompanha "
            "como será a trajetória desse romance!"
        ),
        "detalhes": [
            "Editora: Panini",
            "Data da Publicação: 6 julho 2006",
            "Edição: 1ª",
            "Idioma: Português",
            "Número de páginas: 132 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },
    
    {
        "id": 6,
        "nome": "O menino, a toupeira, a raposa e o cavalo",
        "autor": "Charlie Mackesy",
        "preco": "71,15",
        "imagem": "toupeira.jpg",
        "categoria": "infantojuvenil",
        "ribbon": "Promoção",
        "descricao": (
            "Charlie Mackesy oferece inspiração e esperança neste lindo livro, seguindo a história de "
            "um menino curioso, uma toupeira gananciosa, uma raposa cautelosa e um cavalo sábio que "
            "se encontram em situações às vezes difíceis, compartilhando seus medos e suas descobertas "
            "sobre vulnerabilidade, bondade, esperança, amizade e amor. As aventuras e as conversas "
            "entre os quatro amigos tem tocado leitores de todas as idades, sendo partilhadas na internet, "
            "recriadas em aulas de arte, penduradas nas paredes de hospitais e transformadas em tatuagens."
        ),
        "detalhes": [
            "Editora: Sextante",
            "Data da Publicação: 10 dezembro 2020",
            "Edição: 1ª",
            "Idioma: Português",
            "Número de páginas: 128 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },
    {
        "id": 7,
        "nome": "O Pequeno Príncipe",
        "autor": "Antoine de Saint-Exupéry",
        "preco": "8,55",
        "imagem": "oprincipe.jpg",
        "categoria": "infantojuvenil",
        "ribbon": "Top 4",
        "descricao": (
            "Nesta história que marcou gerações de leitores em todo o mundo, um piloto cai "
            "com seu avião no deserto do Saara e encontra um pequeno príncipe, que o leva a "
            "uma aventura filosófica e poética através de planetas que encerram a solidão humana."
            "Um livro para todos os públicos, O pequeno príncipe é uma obra atemporal, "
            "com metáforas pertinentes e aprendizados sobre afeto, sonhos, esperança e "
            "tudo aquilo que é invisível aos olhos."
        ),
        "detalhes": [
            "Editora: HarpesCollins",
            "Data da Publicação: 1 outubro 2018",
            "Edição: 1ª",
            "Idioma: Português",
            "Número de páginas: 96 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },

    {
        "id": 8,
        "nome": "O Mágico de Oz",
        "autor": "L. Frank Baum",
        "preco": "39,00",
        "imagem": "oz.jpg",
        "categoria": "infantojuvenil",
        "ribbon": "Novo",
        "descricao": (
            "Um ciclone atinge a casa onde Dorothy vive com os tios e ela e seu cachorro Totó são "
            "levados pela ventania e param na Terra de Oz. Por lá, Dorothy faz novos amigos - "
            "o Espantalho, o Lenhador de Lata e o Leão Covarde -, encara perigos, vive histórias "
            "fantásticas e precisa enfrentar seus próprios medos. Depois de tantas aventuras, "
            "a menina descobre que seus Sapatos de Prata têm poderes mágicos e podem levá-la para qualquer parte. "
            "Mas não existe melhor lugar no mundo do que a própria casa."
            "Um clássico indiscutível para todas as idades, a versão impressa apresenta ainda capa dura e "
            "acabamento de luxo."
        ),
        "detalhes": [
            "Editora: Clássicos Zahar",
            "Data da Publicação: 14 fevereiro 2013",
            "Edição: Edição de bolso de Luxo",
            "Idioma: Português",
            "Número de páginas: 224 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },

    # ===== TERROR =====
    {
        "id": 9,
        "nome": "Carrie – Coleção",
        "autor": "Stephen King",
        "preco": "99,90",
        "imagem": "carrie.jpg",
        "categoria": "terror",
        "ribbon": "Novo",
        "descricao": (
            "Carrie White é uma adolescente tímida, solitária e oprimida pela mãe, cristã ferrenha "
            "que vê pecado em tudo. A rotina na escola não alivia o dia a dia em casa. "
            "Para os colegas e professores, ela é estranha, não se encaixa e, por consequência, "
            "é alvo constante de bullying."
        ),
        "detalhes": [
            "Editora: Suma",
            "Data da Publicação: 23 fevereiro 2022",
            "Edição: 1ª",
            "Idioma: Português",
            "Número de páginas: 270 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },
    
    {
        "id": 10,
        "nome": "Ed e Lorraine Warren",
        "autor": "Ed e Lorraine Warren",
        "preco": "55,89",
        "imagem": "warren.jpg",
        "categoria": "terror",
        "ribbon": "Promoção",
        "descricao": (
            "Você tem coragem? Então leia ED & LORRAINE WARREN: DEMONOLOGISTAS, "
            "a biografia definitiva dos mais famosos investigadores paranormais do "
            "nosso plano astral.Não é de hoje que os fãs do terror conhecem Ed Warren e sua esposa, "
            "Lorraine. O casal foi retratado em filmes de grande sucesso, como Invocação do Mal, "
            "Annabelle e Horror em Amityville."
        ),
        "detalhes": [
            "Editora: Darkside Books",
            "Data da Publicação: 6 outubro 2016",
            "Edição: 1ª",
            "Idioma: Português",
            "Número de páginas: 240 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },
    {
        "id": 11,
        "nome": "O Vilarejo",
        "autor": "Raphael Montes",
        "preco": "39,90",
        "imagem": "vilarejo.jpg",
        "categoria": "terror",
        "ribbon": "Top 1",
        "descricao": (
            "Em 1589, o padre e demonologista Peter Binsfeld fez a ligação de cada um dos pecados "
            "capitais a um demônio, supostamente responsável por invocar o mal nas pessoas. "
            "É a partir daí que Raphael Montes cria sete histórias situadas em um vilarejo isolado, "
            "apresentando a lenta degradação dos moradores do lugar, e pouco a pouco o próprio vilarejo "
            "vai sendo dizimado, maculado pela neve e pela fome. As histórias podem ser lidas em "
            "qualquer ordem, sem prejuízo de sua compreensão, mas se relacionam de maneira complexa, "
            "de modo que ao término da leitura as narrativas convergem para uma única e surpreendente "
            "conclusão."
        ),
        "detalhes": [
            "Editora: Suma",
            "Data da Publicação: 14 agosto 2015",
            "Edição: 1ª",
            "Idioma: Português",
            "Número de páginas: 96 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },

    {
        "id": 12,
        "nome": "It – A Coisa",
        "autor": "Stephen King",
        "preco": "46,90",
        "imagem": "it.jpg",
        "categoria": "terror",
        "ribbon": "Novo",
        "descricao": (
            "Durante as férias de 1958, em uma pacata cidadezinha chamada Derry, um grupo de sete "
            "amigos começa a ver coisas estranhas. Um conta que viu um palhaço, outro que viu uma múmia. "
            "Finalmente, acabam descobrindo que estavam todos vendo a mesma coisa: um ser sobrenatural "
            "e maligno que pode assumir várias formas. É assim que Bill, Beverly, Eddie, Ben, Richie, "
            "Mike e Stan enfrentam a Coisa pela primeira vez."
        ),
        "detalhes": [
            "Editora: Suma",
            "Data da Publicação: 24 julho 2014",
            "Edição: 1ª",
            "Idioma: Português",
            "Número de páginas: 1104 páginas"
        ],
        "detalhes_compra": [
            "Frete Grátis",
            "Entrega entre 15 a 20 dias úteis",
            "Devolução em até 15 dias após o recebimento",
            "Vendido por: Loja.com"
        ]
    },

        # ===== CLÁSSICOS =====
        {
            "id": 13,
            "nome": "Crime e Castigo",
            "autor": "Fiodor Dostoievski",
            "preco": "25,90",
            "imagem": "crime-castigo.jpg",
            "categoria": "classicos",
            "ribbon": "Top 3",
            "descricao": (
                "A pobreza assola Raskólnikov, que precisa pagar os estudos e o aluguel de onde mora. "
                "Orgulhoso, acredita que é inteligente o suficiente para planejar um crime perfeito, "
                "julgando que seu bom motivo e futuro promissor justificariam o ato. Os limites da "
                "moralidade comum também o atingem e ele é sentenciado. A culpa o acompanha na jornada "
                "em busca de redenção e boas perspectivas. Dostoiévski traz a psicologia criminal para "
                "este romance, abordando moralidade e a margem da dignidade nas ruas das cidades."
            ),
            "detalhes": [
                "Editora: Principis",
                "Data da Publicação: 3 agosto 2020",
                "Edição: 1ª",
                "Idioma: Português",
                "Número de páginas: 240 páginas"
            ],
            "detalhes_compra": [
                "Frete Grátis",
                "Entrega entre 15 a 20 dias úteis",
                "Devolução em até 15 dias após o recebimento",
                "Vendido por: Loja.com"
            ]
        },
        {
            "id": 14,
            "nome": "A Metamorfose",
            "autor": "Franz Kafta",
            "preco": "22,90",
            "imagem": "metamorfose.jpg",
            "categoria": "classicos",
            "ribbon": "Promoção",
            "descricao": (
                "O caixeiro-viajante Gregor acorda metamorfoseado em um enorme inseto e percebe que tudo "
                "mudou e não só em sua vida, mas no mundo. Ele, então, acompanha as reações de "
                "sua família ao perceberem o estranho ser em que ele se tornou. E, enquanto "
                "luta para se manter vivo, reflete sobre o comportamento de seus pais, de sua "
                "irmã e sobre a sua nova vida"
            ),
            "detalhes": [
                "Editora: Principis",
                "Data da Publicação: 27 setembro 2019",
                "Edição: Integral",
                "Idioma: Português",
                "Número de páginas: 96 páginas"
            ],
            "detalhes_compra": [
                "Frete Grátis",
                "Entrega entre 15 a 20 dias úteis",
                "Devolução em até 15 dias após o recebimento",
                "Vendido por: Loja.com"
            ]
        },
        {
            "id": 15,
            "nome": "Dom Casmurro",
            "autor": "Machado de Assis",
            "preco": "29,90",
            "imagem": "casmurro.jpg",
            "categoria": "classicos",
            "ribbon": "Top 5",
            "descricao": (
                "Em Dom Casmurro, o narrador Bento Santiago retoma a infância que passou na Rua de Matacavalos e "
                "conta a história do amor e das desventuras que viveu com Capitu, uma das personagens mais "
                "enigmáticas e intrigantes da literatura brasileira. Nas páginas deste romance, encontra-se a "
                "versão de um homem perturbado pelo ciúme, que revela aos poucos sua psicologia complexa e enreda "
                "o leitor em sua narrativa ambígua acerca do acontecimento ou não do adultério da mulher com olhos "
                "de ressaca, uma das maiores polêmicas da literatura brasileira."
            ),
            "detalhes": [
                "Editora: Principis",
                "Data da Publicação: 2 maio 2019",
                "Edição: 3ª",
                "Idioma: Português",
                "Número de páginas: 208 páginas"
            ],
            "detalhes_compra": [
                "Frete Grátis",
                "Entrega entre 15 a 20 dias úteis",
                "Devolução em até 15 dias após o recebimento",
                "Vendido por: Loja.com"
            ]
        },
        {
            "id": 16,
            "nome": "O Alienista",
            "autor": "Machado de Assis",
            "preco": "26,62",
            "imagem": "alienista.jpg",
            "categoria": "classicos",
            "ribbon": "Novo",
            "descricao": (
                "Machado de Assis, neste livro, propõe a seguinte pergunta: quem é louco? Conheça a história "
                "do médico Simão Bacamarte, dedicado e estudioso da mente humana, que decide construir um "
                "hospício para tratar os doentes mentais na pequena cidade de Itaguaí a casa verde. Quem "
                "entra e quem fica de fora? Surpreenda-se com o final."
            ),
            "detalhes": [
                "Editora: Principis",
                "Data da Publicação: 19 dezembro 2019",
                "Edição: Questões de vestibular comentadas",
                "Idioma: Português",
                "Número de páginas: 80 páginas"
            ],
            "detalhes_compra": [
                "Frete Grátis",
                "Entrega entre 15 a 20 dias úteis",
                "Devolução em até 15 dias após o recebimento",
                "Vendido por: Loja.com"
            ]
        },
]

if __name__ == "__main__":
    app.run(debug=True)