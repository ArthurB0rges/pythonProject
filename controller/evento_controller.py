from flask import Blueprint, render_template, request, redirect
from model.evento import Evento
from data.memoria import eventos  # A lista contendo os eventos
from dao.evento_dao import EventoDAO

evento_bp = Blueprint("evento", __name__)

@evento_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        evento = Evento(
            request.form["nome"],
            request.form["data"],
            request.form["local"],
            request.form["vagas"],
        )
        
        EventoDAO.salvar(evento)
        return redirect("/")

    lista_eventos = EventoDAO.listar()
        
    # Passa a lista 'eventos' (no plural) importada da memória
    return render_template("index.html", eventos=lista_eventos)