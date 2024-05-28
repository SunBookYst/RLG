from flask import Flask
from .routes.game_routes import game_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(game_routes, url_prefix='/api/game')
    return app