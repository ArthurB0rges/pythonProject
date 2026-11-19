from flask import Blueprint, abort, jsonify, request, session, url_for

from controller.dados_evento import validar_evento
from dao.evento_dao import EventoDAO
from model.evento import Evento

# Aula 15 — O prefixo /api concentra os recursos acessados pelas rotas JSON.
api_bp = Blueprint("api", __name__, url_prefix="/api")


# Aula 15 — A API usa a sessão do login e responde 401 em JSON quando falta autenticação.
@api_bp.before_request
def exigir_login():
    if not session.get("usuario_id"):
        abort(401, "Autenticação necessária.")


# Aula 15 — As rotas de item compartilham a busca e respondem 404 quando o ID não existe.
def buscar_evento(id):
    evento = EventoDAO.buscar_por_id(id)
    if evento is None:
        abort(404, "Evento não encontrado.")
    return evento


# Aulas 14 e 15 — O servidor interpreta JSON e diferencia mídia incorreta (415) de dados inválidos (400).
def ler_dados():
    if not request.is_json:
        abort(415, "Use Content-Type: application/json.")
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        abort(400, "Envie um objeto JSON válido.")
    try:
        return validar_evento(dados)
    except ValueError as erro:
        abort(400, str(erro))


# Aulas 14 e 15 — GET da coleção serializa os registros em JSON e retorna 200.
@api_bp.get("/eventos")
def listar():
    return jsonify([evento.para_dicionario() for evento in EventoDAO.listar()])


# Aula 15 — GET de um item retorna a representação do evento identificado na URL.
@api_bp.get("/eventos/<int:id>")
def buscar(id):
    return jsonify(buscar_evento(id).para_dicionario())


# Aulas 14 e 15 — POST cria um recurso. O 201 e o cabeçalho Location identificam o resultado.
@api_bp.post("/eventos")
def criar():
    evento = Evento(**ler_dados())
    EventoDAO.salvar(evento)
    return jsonify(evento.para_dicionario()), 201, {"Location": url_for("api.buscar", id=evento.id)}


# Aula 15 — PUT substitui os campos. Repetir o mesmo pedido produz o mesmo estado.
@api_bp.put("/eventos/<int:id>")
def atualizar(id):
    evento = buscar_evento(id)
    EventoDAO.atualizar(evento, **ler_dados())
    return jsonify(evento.para_dicionario())


# Aula 15 — DELETE responde 403 para perfil comum e 204 sem corpo após a exclusão.
@api_bp.delete("/eventos/<int:id>")
def excluir(id):
    if session.get("perfil") != "admin":
        abort(403, "Apenas coordenadores podem excluir eventos.")

    EventoDAO.excluir(buscar_evento(id))
    return "", 204
