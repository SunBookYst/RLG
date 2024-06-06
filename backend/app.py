from flask import Flask
from game_routes import game_routes

app = Flask(__name__)

app.register_blueprint(game_routes)

app.run()