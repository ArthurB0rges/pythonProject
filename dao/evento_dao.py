from extensions import db
from model.evento import Evento


# Aulas 9 e 15 — As páginas HTML e a API usam as mesmas operações de persistência.
class EventoDAO:

    # Aula 9 — Create. Adiciona o objeto à sessão do ORM e confirma a gravação.
    @staticmethod
    def salvar(evento):
        db.session.add(evento)
        db.session.commit()

    # Aula 9 — Read. Carrega a lista de eventos em ordem de ID.
    @staticmethod
    def listar():
        return Evento.query.order_by(Evento.id).all()

    # Aula 9 — Read. Busca pela chave primária recebida na rota.
    @staticmethod
    def buscar_por_id(id):
        if id > 2**63 - 1:
            return None
        return db.session.get(Evento, id)

    # Aula 9 — Update. O ORM registra os atributos alterados e grava no commit.
    @staticmethod
    def atualizar(evento, nome, data, local, vagas):
        evento.nome = nome
        evento.data = data
        evento.local = local
        evento.vagas = vagas
        db.session.commit()

    # Aula 9 — Delete. A exclusão do objeto é confirmada na mesma transação.
    @staticmethod
    def excluir(evento):
        db.session.delete(evento)
        db.session.commit()
