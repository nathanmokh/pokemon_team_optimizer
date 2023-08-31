from flask import Flask, abort
from flask import jsonify
from config import Config
from extensions import db
from pokebuilder.sql.scripts.get_pokemon_moveset import get_pokemon_moveset_endpoint
from flask import request

app = Flask(__name__)
app.config.from_object(obj=Config)

# Extensions

db.init_app(app)


# Routes


@app.route("/")
def get_random_pokemon():
    return jsonify(message="Pokebuilder")


@app.route("/api/getPokemonMoveset")
def get_moves_for_pokemon():
    args = request.args
    pokemon_id = args.get("pokemon_id")
    game_version = args.get("game_version")
    if not game_version:
        abort(400, "Missing game_version parameter")
    return get_pokemon_moveset_endpoint(pokemon_id, game_version)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
