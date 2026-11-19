from extensions import db


# Aula 11 (revisão de modelagem) — A inscrição liga um participante a um evento.
# A restrição única permite uma inscrição por par de IDs.
class Inscricao(db.Model):
    __table_args__ = (db.UniqueConstraint("participante_id", "evento_id"),)

    id = db.Column(db.Integer, primary_key=True)
    participante_id = db.Column(
        db.Integer, db.ForeignKey("participante.id"), nullable=False
    )
    # Aula 9 — A chave com CASCADE remove as inscrições associadas na exclusão de um evento.
    evento_id = db.Column(
        db.Integer, db.ForeignKey("evento.id", ondelete="CASCADE"), nullable=False
    )
    data_inscricao = db.Column(db.Date, nullable=False)
