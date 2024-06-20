from flask import Blueprint, request, jsonify
from backendsys import BackEndSystem, MultiThreadManager


bs = BackEndSystem()
monitor = MultiThreadManager(bs)

# 注册一个路由，马上启动！
game_routes = Blueprint('game_routes', __name__)

@game_routes.route('/signup', methods=['GET'])
def register():
    data = request.json
    res = bs.registerPlayer(name     = data["username"], 
                            email    = data["email"],
                            password = data["password"])

    if res:
        # 返回一个 JSON 响应
        return jsonify({
            'status_code': 200,
        })
    else:
        # 返回一个 JSON 响应
        return jsonify({
            'status_code': 404,
        })


@game_routes.route('/login', methods=['GET'])
def login():
    # 返回200代表登陆成功，返回404代表邮箱或密码不正确
    data = request.json
    user_name = bs.loginPlayer( email    = data["email"], 
                                password = data["password"])
    if user_name:
        return jsonify({
            'status_code': 200,
            'username': user_name
        })
    else:
        return jsonify({
            'status_code': 404,
            'username': None
        })

@game_routes.route('/main', methods=['GET'])
def interact_with_dm():
    data = request.json
    response = bs.getPlayerInput(player_name = data["role"],
                                player_input = data["text"],
                                mode         = 0)

    return response


@game_routes.route('/select', methods=['GET'])
def select_task():
    data = request.json
    # What happens when the player selects a task?
    task_response = bs.selectTask(player_name = data["role"], 
                                task_name     = data["task_name"])
    return task_response

@game_routes.route('/feedback', methods=['GET'])
def interact_with_task():
    data = request.json
    task_response = \
    bs.getPlayerInput(player_name    = data["role"],
                    player_input = data["text"],
                    mode         = 1,
                    roles        = data["roles"],
                    equipment    = data["items"],
                    skill        = data["skills"])

    return task_response


@game_routes.route('/task_info', methods=['GET'])
def get_all_tasks():
    data = request.json
    response = bs.getAllAvailableTasks()
    return jsonify({'task_list': response})


@game_routes.route('/status', methods=['GET'])
def get_player_info():
    data = request.json
    # well that's...
    response = bs.getPlayerInfo(data["role"])
    return jsonify({'attribute': response})


@game_routes.route('/bag', methods=['GET'])
def get_player_bag():
    data = request.json
    return jsonify({"equipments": bs.player_dict[data['role']].bag})


@game_routes.route('/skill', methods=['GET'])
def get_player_skill():
    data = request.json
    return jsonify({"skills": bs.player_dict[data['role']].skills})


@game_routes.route('/merge', methods=['GET'])
def get_an_item():
    data = request.json
    response = bs.craftItems(player_name = data["role"], 
                            mode         = data["mode"],
                            num          = data["num"],
                            description  = data["des"])

    return jsonify({'text': response})

@game_routes.route('/task_request', methods=['GET'])
def customize_a_task():
    data = request.json
    response = bs.taskCustomize(player_name = data["role"], 
                                description = data["text"])

    return jsonify({'text': response})


@game_routes.route('/task_info_personal', methods=['GET'])
def get_all_customized_tasks():
    data = request.json
    response = bs.getAllAvailablePersonalTasks(data["role"])

    return jsonify({'task_list': response})

# ! This changed.
@game_routes.route('/select_personal', methods=['GET'])
def select_customized_task():
    data = request.json
    task_response, task_bg = bs.selectPersonalTask(player_name=data["role"], task_name=data["task_name"])

    return task_response

@game_routes.route('/battle', methods=['GET'])
def battle_with_player():
    """
    
    We provide the data as:
    {
        "role": "player_name",
        "action": "description"
    }

    The expected outcome as:
    {
        "role": "oppoment_name", 对手用户名
        "action": "description", 对手的行为描述
        "result": "description"  系统对战斗行为的描述。
    }
    """
    data = request.json

    return jsonify({'role': '',
                    'action': '',
                    'result': ''})


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

