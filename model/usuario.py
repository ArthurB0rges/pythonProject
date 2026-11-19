from extensions import db


# Aula 13 — O e-mail único identifica a conta e o perfil determina a permissão de excluir eventos.
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Aula 13 — O banco guarda o hash usado para verificar a senha no login.
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default="comum")
