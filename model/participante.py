from extensions import db

class Participante(db.Model):
    id    = db.Column(db.Integer, primary_key=True)
    nome  = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)