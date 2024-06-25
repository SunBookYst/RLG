from flask import Flask
from game_routes import game_routes

from util.constant import FLASK_SERVER

if __name__ == "__main__":

    app = Flask(__name__)
    app.register_blueprint(game_routes)

    ip, port = FLASK_SERVER
    app.run(host=ip, port=port, threaded=True)
