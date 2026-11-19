import os
from secrets import token_hex
from threading import Lock

from flask import Flask, request
from sqlalchemy import event, inspect
from werkzeug.exceptions import HTTPException

from controller.api_controller import api_bp
from controller.auth_controller import auth_bp, criar_admin
from controller.evento_controller import evento_bp
from extensions import db
from model import inscricao, participante  # Registra as tabelas do DER no ORM.
from model.evento import Evento


# Aula 9 — A exclusão de eventos depende das chaves estrangeiras para remover as inscrições vinculadas.
def ativar_chaves_estrangeiras(conexao, _):
    conexao.execute("PRAGMA foreign_keys=ON")


# Aula 11 (revisão de persistência) — A inicialização prepara o SQLite usado pelos DAOs.
def preparar_banco():
    with db.engine.begin() as conexao:
        # Serializa a atualização do esquema e mantém a cópia dos dados na transação.
        conexao.exec_driver_sql("BEGIN IMMEDIATE")
        esquema = inspect(conexao)
        if esquema.has_table("evento"):
            colunas = {coluna["name"] for coluna in esquema.get_columns("evento")}
            if not {"local", "vagas"} <= colunas:
                # A versão antiga ainda não tinha a tabela de inscrições.
                conexao.exec_driver_sql("ALTER TABLE evento RENAME TO evento_legado")
                Evento.__table__.create(conexao)
                local = "local" if "local" in colunas else "''"
                vagas = "vagas" if "vagas" in colunas else "0"
                conexao.exec_driver_sql(
                    "INSERT INTO evento (id, nome, data, local, vagas) "
                    f"SELECT id, nome, data, {local}, {vagas} FROM evento_legado"
                )
                conexao.exec_driver_sql("DROP TABLE evento_legado")

        db.metadata.create_all(conexao)


def create_app(config=None):
    app = Flask(__name__)
    # Aulas 10 e 12 — O Flask usa a chave para assinar a sessão que carrega os flashes e o login.
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or token_hex(32),
        SQLALCHEMY_DATABASE_URI="sqlite:///banco.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    if config:
        app.config.update(config)

    db.init_app(app)
    # Aula 12 — O total de acessos pertence à aplicação e é compartilhado entre as sessões.
    app.extensions["acessos"] = {"total": 0, "lock": Lock()}
    # Aulas 9, 13 e 15 — Cada Blueprint registra as rotas de eventos, autenticação e API.
    app.register_blueprint(evento_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.cli.add_command(criar_admin)

    # Aula 15 — As recusas da API mantêm o status HTTP e devolvem um objeto JSON com a mensagem.
    @app.errorhandler(HTTPException)
    def tratar_erro(erro):
        if request.path == "/api" or request.path.startswith("/api/"):
            resposta = erro.get_response()
            resposta.set_data(app.json.dumps({"erro": erro.description}))
            resposta.mimetype = "application/json"
            return resposta
        return erro

    with app.app_context():
        event.listen(db.engine, "connect", ativar_chaves_estrangeiras)
        preparar_banco()

    return app


if __name__ == "__main__":
    create_app().run()
