from extensions import db

# Aula 11 (revisão de modelagem e ORM) — O ID do participante identifica a pessoa nas inscrições.
class Participante(db.Model):
    id    = db.Column(db.Integer, primary_key=True)
    nome  = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
