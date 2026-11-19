from sqlalchemy.exc import IntegrityError

from extensions import db
from model.usuario import Usuario


# Aula 13 — O controller usa o DAO para buscar a conta por e-mail e gravar o cadastro.
class UsuarioDAO:
    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def salvar(usuario):
        db.session.add(usuario)
        try:
            db.session.commit()
        except IntegrityError:
            # Aula 13 — Em caso de e-mail duplicado, a transação é desfeita e o controller trata a recusa.
            db.session.rollback()
            raise
