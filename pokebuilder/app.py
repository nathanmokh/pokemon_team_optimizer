from flask import Flask
from config import Config
from extensions import db
from pokebuilder.routes.pokemon_info import pokemon_routes

app = Flask(__name__)
app.config.from_object(obj=Config)

# Extensions

db.init_app(app)


# Blueprints

app.register_blueprint(pokemon_routes)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
