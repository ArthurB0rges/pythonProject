from extensions import db
from model.evento import Evento

class EventoDAO:

    @staticmethod
    def salvar(evento):
        db.session.add(evento)
        db.session.commit()

    @staticmethod
    def listar():
        return Evento.query.all()