from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Olá, mundo!"

@app.route("/sobre")
def sobre():
    return "Tu é?"

@app.route("/eventos")
def eventos():
    return "Sai daqui meu!"


if __name__ == "__main__":
    app.run(debug=True)