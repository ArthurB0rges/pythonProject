import re

import click
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from dao.usuario_dao import UsuarioDAO
from model.usuario import Usuario

# Aula 13 — Este Blueprint reúne as rotas de entrada, cadastro e saída.
auth_bp = Blueprint("auth", __name__)


# Aula 13 — O servidor valida os campos e gera o hash antes de gravar a conta.
def registrar_usuario(nome, email, senha, perfil):
    if not nome or len(nome) > 120:
        raise ValueError("Informe um nome com até 120 caracteres.")
    if len(email) > 120 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("Informe um e-mail válido.")
    if not 6 <= len(senha) <= 128:
        raise ValueError("A senha deve ter de 6 a 128 caracteres.")

    usuario = Usuario(nome=nome, email=email, senha_hash=generate_password_hash(senha), perfil=perfil)
    try:
        UsuarioDAO.salvar(usuario)
    except IntegrityError:
        raise ValueError("Já existe uma conta com esse e-mail.") from None


# Aula 13 — Busca a conta pelo e-mail e verifica a senha fornecida usando o hash armazenado.
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    email = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = UsuarioDAO.buscar_por_email(email)
        if usuario and 6 <= len(senha) <= 128 and check_password_hash(usuario.senha_hash, senha):
            # Aulas 12 e 13 — O login reinicia a sessão e grava o ID, o nome e o perfil da conta.
            session.clear()
            session["usuario_id"] = usuario.id
            session["nome"] = usuario.nome
            session["perfil"] = usuario.perfil
            return redirect(url_for("evento.index"))
        flash("E-mail ou senha inválidos.", "erro")

    return render_template("login.html", email=email)


# Aula 13 — O cadastro público cria uma conta de perfil comum. Os flashes da Aula 10 dão o retorno.
@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    nome = email = ""
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        try:
            registrar_usuario(nome, email, request.form.get("senha", ""), "comum")
        except ValueError as erro:
            flash(str(erro), "erro")
        else:
            flash("Conta criada. Entre com seu e-mail e sua senha.", "sucesso")
            return redirect(url_for("auth.login"))

    return render_template("cadastro.html", nome=nome, email=email)


# Aulas 12 e 13 — Sair limpa o estado da sessão e encerra o acesso às rotas protegidas.
@auth_bp.post("/sair")
def sair():
    session.clear()
    return redirect(url_for("auth.login"))


# Aula 13 — O comando de terminal cria uma conta de coordenação para exercitar as permissões.
@click.command("criar-admin")
@click.option("--nome", default="Coordenação", show_default=True)
@click.option("--email", prompt=True)
@click.password_option("--senha", prompt="Senha")
@with_appcontext
def criar_admin(nome, email, senha):
    """Cria uma conta de coordenação no banco local."""
    try:
        registrar_usuario(nome.strip(), email.strip().lower(), senha, "admin")
    except ValueError as erro:
        raise click.ClickException(str(erro)) from erro
    click.echo("Conta de coordenação criada.")
