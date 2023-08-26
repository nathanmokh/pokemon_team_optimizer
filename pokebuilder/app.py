from flask import Flask
from flask import jsonify
from config import Config
from extensions import db
from pokebuilder.sql.scripts.get_pokemon_moveset import get_pokemon_moveset_query

app = Flask(__name__)
app.config.from_object(obj=Config)

# Extensions

db.init_app(app)


# Routes


@app.route("/")
def random_pokemon():
    return jsonify(message="Pokebuilder")

@app.route("/get_moves/<int:pokemon_id>/<string:game_version>")
def get_moves_for_pokemon(pokemon_id, game_version):
    query = get_pokemon_moveset_query(app, pokemon_id, game_version)
    result = query.all()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
