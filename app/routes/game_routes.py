from flask import Blueprint, request, jsonify
from RLG.app.services.backend import backend


# 实例化 backend
backend_instance = backend(time_set=40, debug=True)

game_routes = Blueprint('game_routes', __name__)

#生成任务,传入任务类别和描述
@game_routes.route('/generate_task',method=['POST'])
def gtask():
    data=request.json
    backend_instance.generate_task(data)

#接收任务,传入任务名
@game_routes.route('/accept',method=['POST'])
def acpt():
    task_name=request.json.get('task_name')
    response = backend_instance.accept(task_name)
    return response

#初始化系统,传入玩家信息
@game_routes.route('/init', methods=['POST'])
def init():
    data = request.json
    response = backend_instance.init(data)
    return jsonify(response), 200

#任务清单
@game_routes.route('/tasks', methods=['GET'])
def get_task_info():
    response=backend_instance.quest_list
    return response
#玩家信息
@game_routes.route('/player_data', methods=['POST'])
def get_pl_info():
    data = request.json
    response = backend_instance.pl_data[data.get('role')]
    return response
#时间信息
@game_routes.route('/time', methods=['GET'])
def get_game_time():
    game_time = backend_instance.get_game_time()
    return jsonify({"game_time": game_time}), 200
#对话函数
@game_routes.route('/main', methods=['POST'])
def chat():
    data = request.json
    response = backend_instance.chat(data)
    return jsonify(response), 200
#保存,提供路径
@game_routes.route('/save', methods=['POST'])
def save_game():
    filename = request.json.get('filename', 'game_state.pkl')
    backend_instance.save(filename)
    return jsonify({"status": f"游戏状态已保存到 {filename}"}), 200
#读取,提供路径
@game_routes.route('/load', methods=['POST'])
def load_game():
    filename = request.json.get('filename', 'game_state.pkl')
    global backend_instance
    backend_instance = backend.load(filename)
    return jsonify({"status": f"游戏状态已从 {filename} 加载"}), 200
