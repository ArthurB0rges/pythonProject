from extensions import db


# Aula 11 (revisão do ORM) — Cada objeto Evento representa um registro da tabela usada pelo CRUD.
class Evento(db.Model):
    # Aula 15 — O SQLite gera o ID de cada recurso e evita reutilizar IDs de registros excluídos.
    __table_args__ = {"sqlite_autoincrement": True}

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    local = db.Column(db.String(120), nullable=False, default="")
    vagas = db.Column(db.Integer, nullable=False, default=0)

    # Aula 14 — O dicionário reúne os campos que jsonify() envia ao navegador e à API da Aula 15.
    def para_dicionario(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data": self.data,
            "local": self.local,
            "vagas": self.vagas,
        }
