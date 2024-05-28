from flask import Blueprint, request, jsonify
from ..services.backend import backend
from ..prompts import prompt
# 实例化 backend
backend_instance = backend(prompt.background, time_set=40, debug=True)

game_routes = Blueprint('game_routes', __name__)

@game_routes.route('/start_game', methods=['POST'])
def start_game():
    backend_instance.start_game()
    return jsonify({"status": "游戏已开始"}), 200

@game_routes.route('/pause_game', methods=['POST'])
def pause_game():
    backend_instance.pause_game()
    return jsonify({"status": "游戏已暂停"}), 200

@game_routes.route('/get_game_time', methods=['GET'])
def get_game_time():
    game_time = backend_instance.get_game_time()
    return jsonify({"game_time": game_time}), 200

@game_routes.route('/chat', methods=['POST'])
def chat():
    data = request.json
    response = backend_instance.chat(data)
    return jsonify(response), 200

@game_routes.route('/save', methods=['POST'])
def save_game():
    filename = request.json.get('filename', 'game_state.pkl')
    backend_instance.save(filename)
    return jsonify({"status": f"游戏状态已保存到 {filename}"}), 200

@game_routes.route('/load', methods=['POST'])
def load_game():
    filename = request.json.get('filename', 'game_state.pkl')
    global backend_instance
    backend_instance = backend.load(filename)
    return jsonify({"status": f"游戏状态已从 {filename} 加载"}), 200
