from flask import (
    Blueprint, abort, current_app, flash, redirect, render_template, request,
    session, url_for,
)

from controller.dados_evento import validar_evento
from dao.evento_dao import EventoDAO
from model.evento import Evento

evento_bp = Blueprint("evento", __name__)


# Aula 13 — Todas as rotas HTML de eventos exigem login e redirecionam para a tela de entrada.
@evento_bp.before_request
def exigir_login():
    if not session.get("usuario_id"):
        return redirect(url_for("auth.login"))


# Aula 9 — GET lista os eventos. POST cadastra e redireciona para um novo GET (Post/Redirect/Get).
# Aula 14 — O POST HTML também atende quem envia o formulário com JavaScript desativado.
@evento_bp.route("/", methods=["GET", "POST"])
def index():
    dados = {}
    if request.method == "POST":
        dados = request.form
        try:
            evento = Evento(**validar_evento(dados, formulario=True))
        except ValueError as erro:
            flash(str(erro), "erro")
        else:
            EventoDAO.salvar(evento)
            flash("Evento cadastrado.", "sucesso")
            return redirect(url_for("evento.index"))

    # Aula 12 — Cada GET da página incrementa a visita da sessão e o total da aplicação.
    acessos = current_app.extensions["acessos"]
    if request.method == "GET":
        session["visitas"] = session.get("visitas", 0) + 1
        with acessos["lock"]:
            acessos["total"] += 1

    # Aulas 10 e 12 — O template recebe os eventos do DAO e lê a preferência armazenada no cookie.
    return render_template(
        "index.html", eventos=EventoDAO.listar(), dados=dados,
        exibicao=request.cookies.get("exibicao", "completa"), acessos=acessos["total"],
    )


# Aula 9 — O parâmetro identifica o evento. GET preenche o formulário e POST salva a edição.
@evento_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    evento = EventoDAO.buscar_por_id(id)
    if evento is None:
        abort(404)

    dados = evento.para_dicionario()
    if request.method == "POST":
        dados = request.form
        try:
            campos = validar_evento(dados, formulario=True)
        except ValueError as erro:
            flash(str(erro), "erro")
        else:
            EventoDAO.atualizar(evento, **campos)
            flash("Evento atualizado.", "sucesso")
            return redirect(url_for("evento.index"))

    return render_template("editar.html", dados=dados)


# Aula 9 — A exclusão HTML usa POST para que abrir um link nunca apague registros.
@evento_bp.post("/excluir/<int:id>")
def excluir(id):
    # Aula 13 — O servidor confere o perfil antes de remover o evento.
    if session.get("perfil") != "admin":
        flash("Apenas coordenadores podem excluir eventos.", "erro")
        return redirect(url_for("evento.index"))

    evento = EventoDAO.buscar_por_id(id)
    if evento is None:
        abort(404)
    EventoDAO.excluir(evento)
    flash("Evento excluído.", "sucesso")
    return redirect(url_for("evento.index"))


# Aula 12 — A preferência visual fica em um cookie de 30 dias, enviado junto com o redirecionamento.
@evento_bp.post("/preferencia")
def preferencia():
    modo = request.form.get("modo")
    if modo not in ("compacta", "completa"):
        abort(400)
    resposta = redirect(url_for("evento.index"))
    resposta.set_cookie("exibicao", modo, max_age=30 * 24 * 60 * 60, samesite="Lax")
    return resposta
