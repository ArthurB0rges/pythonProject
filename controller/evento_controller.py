

evento_bp = Blueprint("evento", __name__);

@evento_bp.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        evento = Evento();
        eventos.append(evento)
        return redirect("/")
    return render_template("index.html", eventos=eventos)
