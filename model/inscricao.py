class Inscricao:
    def __init__(self, participante_id, evento_id, data_inscricao, id=None):
        self.id = id
        self.participante_id = participante_id   # referência ao Participante
        self.evento_id = evento_id               # referência ao Evento
        self.data_inscricao = data_inscricao