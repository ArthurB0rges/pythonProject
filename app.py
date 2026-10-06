# app.py
from flask import Flask
from controller.evento_controller import evento_bp
from extensions import db
from model.participante import Participante  # <-- 1. Import do modelo

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão 'db' no Flask
db.init_app(app)

app.register_blueprint(evento_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        p1 = Participante(nome="Maria", email="maria@exemplo.com")
        p2 = Participante(nome="Joao", email="joao@exemplo.com")
        p3 = Participante(nome="Pedro", email="pedro@exemplo.com")
        
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.commit()

        todos = Participante.query.all()
        um = db.session.get(Participante, 1)
        filtro = Participante.query.filter_by(nome="Maria").all()

    app.run(debug=True)