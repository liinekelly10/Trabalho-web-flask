from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)  # <- novo
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    # Cria o hash da senha
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    # Verifica a senha no login
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    # Retorna dados sem a senha (segurança)
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "username": self.username,
            "email": self.email
        }
