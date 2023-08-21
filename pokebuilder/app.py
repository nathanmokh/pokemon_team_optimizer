from flask import Flask
from flask import jsonify
from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(obj=Config)

# Extensions

db.init_app(app)


# Routes


@app.route("/")
def random_pokemon():
    return jsonify(message="Pokebuilder")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
