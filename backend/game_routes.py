from flask import Blueprint, request, jsonify
from backendsys import BackEndSystem


# 实例化 backend
backend_instance = None

bs = BackEndSystem()

# 注册一个路由，马上启动！
game_routes = Blueprint('game_routes', __name__)


@game_routes.route('/main', methods=['GET'])
def interact_with_dm():
    """
    data is 
    {
        'text':str,
        'role':str
    }

    returns
    {
        'text':str,
        'role':str,
        'status':bool,
    }
    """
    data = request.json
    response, __ = bs.getPlayerInput(player_name = data["role"], player_input = data["text"])

    # ?What is this thing...

    return response

@game_routes.route('/feedback', methods=['GET'])
def interact_with_task():
    data = request.json
    
    # TODO judge and task is not accordant.
    # TODO bs do not make the rewards...

    judge_response, task_response = bs.getPlayerInput(player_name = data["role"], player_input = data["text"])

    print('[server]',task_response)

    return task_response

@game_routes.route('/task_info', methods=['GET'])
def get_all_tasks():
    data = request.json
    return {'task_list': bs.getAllAvailableTasks(data["role"]) }

@game_routes.route('/status', methods=['GET'])
def get_player_info():
    data = request.json

    response = bs.getPlayerInfo(data["role"])


    return {'attribute': response}

@game_routes.route('/bag', methods=['GET'])
def get_player_bag():
    data = request.json

    return {'equipments':[]}

    return {'equipment': bs.player_dict[data['role']].bag}


@game_routes.route('/skill', methods=['GET'])
def get_player_skill():
    return {'skills': []}

@game_routes.route('/time', methods=['GET'])
def get_user_time():
    data = request.json

    return {'time': bs.getPlayerTime(data["role"])}

@game_routes.route('/legal', methods=['GET'])
def check_name_legal():
    data = request.json
    if data["mode"] == 0:
        response = bs.checkNameValid(data["content"])
    elif data["mode"] == 1:
        response = bs.checkFeatureValid(data["content"])
    else:
        return {'status':False}
    return {'status':response}

@game_routes.route('/merge', methods=['GET'])
def get_an_item():
    data = request.json
    response = bs.craft_items(data["role"], data["mode"], data["num"], data["des"])

    return {'text': response["outlook"]}

# TODO: save and load.
# @game_routes.route('/save', methods=['POST'])
# def save_game():
#     filename = request.json.get('filename', 'game_state.pkl')
#     backend_instance.save(filename)
#     return jsonify({"status": f"游戏状态已保存到 {filename}"}), 200

# #读取,提供路径
# @game_routes.route('/load', methods=['POST'])
# def load_game():
#     filename = request.json.get('filename', 'game_state.pkl')
#     global backend_instance
#     backend_instance = backend.load(filename)
#     return jsonify({"status": f"游戏状态已从 {filename} 加载"}), 200





# #生成任务,传入任务类别和描述
# @game_routes.route('/generate_task',method=['POST'])
# def gtask():
#     data=request.json
#     backend_instance.generate_task(data)

# #接收任务,传入任务名
# @game_routes.route('/accept',method=['POST'])
# def acpt():
#     task_name=request.json.get('task_name')
#     response = backend_instance.accept(task_name)
#     return response

# #初始化系统,传入玩家信息
# @game_routes.route('/init', methods=['POST'])
# def init():
#     data = request.json
#     response = backend_instance.init(data)
#     return jsonify(response), 200

# #任务清单
# @game_routes.route('/tasks', methods=['GET'])
# def get_task_info():
#     response=backend_instance.quest_list
#     return response
# #玩家信息
# @game_routes.route('/player_data', methods=['POST'])
# def get_pl_info():
#     data = request.json
#     response = backend_instance.pl_data[data.get('role')]
#     return response
# #时间信息
# @game_routes.route('/time', methods=['GET'])
# def get_game_time():
#     game_time = backend_instance.get_game_time()
#     return jsonify({"game_time": game_time}), 200
# #对话函数
# @game_routes.route('/main', methods=['POST'])
# def chat():
#     data = request.json
#     response = backend_instance.chat(data)
#     return jsonify(response), 200
#保存,提供路径

