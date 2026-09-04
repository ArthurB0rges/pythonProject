# app.py
from flask import Flask
from controller.evento_controller import evento_bp

app = Flask(__name__)
app.register_blueprint(evento_bp)

if __name__ == "__main__":
    app.run(debug=True)