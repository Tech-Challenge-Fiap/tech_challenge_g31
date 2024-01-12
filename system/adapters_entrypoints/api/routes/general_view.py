from app import app

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"