class Participante:
    def __init__(self, nome, email, id=None):
        self.id = id        # chave primária (recebe valor ao persistir)
        self.nome = nome
        self.email = email