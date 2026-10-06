from extensions import db

class Evento(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    data = db.Column(db.String(10),  nullable=False)
    local = db.Column(db.String(10),  nullable=False)
    vagas = db.Column(db.Integer(10),  nullable=False)