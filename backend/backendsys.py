import sys
from datetime import datetime
import random
import time
import threading
import pickle

from subsenario.utils import *
from request import LLMAPI, StableDiffusion


DEBUG = True
sys.path.append('..')


def fixResponse(origin_text: str, attr: str):
    """
    处理LLM所返回内容中潜在的格式错误
    Args:
        origin_text:大模型直接返回的文本
        attr:需要修复的元素
    Returns:
    处理好的文本
    """
    index = origin_text.find(attr)
    if index == -1:
        return origin_text
    else:
        lquote = origin_text.find('"', index + len(attr) + 1)
        rquote = origin_text.find('"', lquote + 1)
        content = origin_text[lquote: rquote + 1]
        print(content)
        content = "\\n".join(content.split("\n"))
        text = origin_text[:lquote] + content + origin_text[rquote + 1:]

        return text


def read_file(prompt_name):
    """
    read the file name.
    Args:
        prompt_name (str): the file name of the prompt stored.

    Returns:
        str: the content of the file.
    """
    with open(f"../prompts/{prompt_name}.txt", 'r', encoding='utf-8') as file:
        prompt = file.read()
    return prompt


class Player(object):
    """
    A class to gather all the information of the player.
    """

    def __init__(self, name: str, email: str, password: str, DM_model: LLMAPI):
        self.name: str = name
        self.email: str = email
        self.password: str = password

        self.feature: str = "【苍穹】大陆上的游戏角色，目前是一个健全的人"
        self.attributes: dict = {
            "龙眼": 0,
            "凤羽": 0,
            "经验值": 0,
        }
        # 玩家的DM
        self.dm_model: LLMAPI = DM_model

        # 玩家的任务系统
        self.task_director: LLMAPI = None
        self.task_judge: LLMAPI = None
        self.task_focus: bool = False
        self.current_task: str = None

        # 玩家的个性化任务
        self.personal_task_queue = {}

        # 玩家的物资
        self.bag: dict = {}
        self.skills: dict = {}
        self.custom_tasks: list = []

    def takeOnTask(self, task_director, judge, task_name):
        self.task_focus = True
        self.task_director = task_director
        self.task_judge = judge
        self.current_task = task_name

    def takeOffTask(self):
        self.task_focus = False
        self.task_director = None
        self.task_judge = None
        task_name = self.current_task
        self.current_task = None
        return task_name

    def talk_to_dm(self, player_input: str):
        """
        based on the input to generate a response.

        Args:
            player_input (str): the user input.

        Returns:
            dict{}: the response from DM/judge
            dict{}/empty dict: The response from the task generator if the user is on task.
        """
        if DEBUG:
            print("conversation with DM")

        response = self.dm_model.generateResponse(f'【玩家】{player_input}')
        print(response)
        response = json.loads(response)

        return response

    def talk_to_director(self, player_input: str, player_use: dict):
        # 跟任务演绎系统交谈
        if DEBUG:
            print("conversation with task")

        # 获取系统最新发言与玩家发言，进入裁判系统判断后演绎新的一幕
        play_infos = {}
        system_words = self.task_director.getAllConversation()[-1]["content"]
        play_infos["system"] = system_words
        play_infos["player"] = player_input
        play_infos["player_status"] = self.attributes | {"character": self.feature} | {"use": player_use}
        content = json.dumps(play_infos, ensure_ascii=False)

        response = self.task_judge.generateResponse(content)

        judge = json.loads(response)

        task_play = {}
        task_play["player"] = player_input
        task_play["judge"] = judge["judge"]
        task_play["reason"] = judge["reason"]

        content = json.dumps(task_play, ensure_ascii=False)

        response = self.task_director.generateResponse(content)
        response = fixResponse(response, "text")

        if DEBUG:
            print('[judge]\n', response)
            print('=' * 10)
            print(content)
            print('[task]\n', response)
            with open("./debug.txt", "w", encoding='utf-8') as f:
                f.write(response)
            print('=' * 10)

        play = json.loads(response)

        return judge, play

    def getReward(self, rewards):
        for k, v in rewards.items():
            self.attributes[k] += v

    def consumeProperty(self, item, num):
        self.attributes[item] -= num

    def organize_player_use(self, equipment_list: list, skill_list: list):
        result = {}

        matching_equipment = [equip for equip in equipment_list if equip in self.bag]
        matching_skill = [s for s in skill_list if s in self.skills]

        result['equipment'] = matching_equipment
        result['skill'] = matching_skill

        return result


class BackEndSystem(object):
    """
    The backend system of the game, mainly maintain the critical information of the game.

    Attributes:
    ---
        - task_generator (List[LLMAPI]) the list of the task generator.
        - bg_generator (List[LLMAPI]) the list of the background generator.
        - sd (List[StableDiffusion]) the list of the image generator.
        - _queue_list (dict{str:list[]}) the task sequence.
        - _sub_model_dict (dict{str:str}) the sub models used.

        - _attribute3_ (type): _description_

    Methods:
    ---
        _method1_ (type): _description_
        _method2_ (type): _description_
        _method3_ (type): _description_
    """

    def __init__(self, one_day_length_minutes=40):
        """
        Args:
            one_day_length_minutes (int, optional): How long a day in the game in minutes. Defaults to 40.
        """

        task_prompt = read_file("task")
        eq_prompt = read_file('equipment_craft')
        sk_prompt = read_file('skill_generate')
        custom_prompt = read_file('task_custom')

        # 以用户名为键值
        self.player_dict: dict[str:Player] = {}
        # 以邮箱为键值
        self.player_dict2: dict[str:Player] = {}
        # 当前在线玩家
        self.online_player: dict[str:Player] = {}

        # 各组件初始化
        self.task_generator: LLMAPI = initialize_llm(task_prompt)
        self.equipment_generator: LLMAPI = initialize_llm(eq_prompt)
        self.skill_generator: LLMAPI = initialize_llm(sk_prompt)
        self.task_custom: LLMAPI = initialize_llm(custom_prompt)
        self.sd: StableDiffusion = StableDiffusion()
        self.sd.initialize()

        # 任务队列
        self.task_queue = {}

        self.start_time = datetime.now()

    def register_player(self, name, email, password):
        """
        Add a new instance of Player in the DM.
        The name and the feature are first checked.

        Args:
            name (str): The player name.
            feature (str): The player's description.
        """
        if name in self.player_dict:
            return False
        if email in self.player_dict2:
            return False

        dm_prompt = read_file("DM")
        dm_model: LLMAPI = initialize_llm(dm_prompt)
        new_player = Player(name, email, password, dm_model)

        self.player_dict[name] = new_player
        self.player_dict2[email] = new_player

        return True

    def login_player(self, email, password):
        player: Player = self.player_dict2[email]
        if password != player.password:
            return None
        else:
            return player.name

    def refresh_task_queue(self, num=3):
        task_type = ["互动任务", "助人任务", "好汉任务", "豪杰任务", "英雄任务", "救世主任务"]
        probabilities = [0.20, 0.20, 0.25, 0.20, 0.15, 0.00]

        # 使用random.choices根据给定的概率选取项
        for i in range(num):
            chosen_item = random.choices(task_type, weights=probabilities, k=1)[0]
            task = self.task_generate(chosen_item)
            self.task_queue[task["task_name"]] = task

    def task_generate(self, task_type, description="任意"):
        """
        Generate a task based on the task type and description.

        Args:
            task_generator (LLMAPI): The task generator.
            task_type (str): the type of the task
            description (str, optional): The detailed description of the task. Defaults to "任意".

        Returns:
            dict{}: The information of generated task.
            {
                "task_name":（任务名称）
                "task_description":（任务描述)
                "attention":（注意事项）
                "reward":（任务报酬）
                "occupied":（是否被占用）
                "player":（占用者）
            }
        """
        need = f"帮我生成一个{description}的{task_type}"
        task = self.task_generator.generateResponse(need, stream=True)
        task = json.loads(task)
        task["occupied"] = False
        task["player"] = None
        return task

    def task_customize(self, player_name, description="任意"):
        need = f"【玩家】帮我生成一个任务， 要求是{description}"
        task = self.task_custom.generateResponse(need, stream=True)
        task = json.loads(task)
        player: Player = self.player_dict[player_name]
        player.personal_task_queue[task['task_name']] = task
        return task

    def get_player_input(self, player_name: str, player_input: str, mode: int, equipment: list, skill: list, roles: list):
        """
        Get the player input and return the response from the DM.

        Args:
            player_name (str): The name of the player.
            player_input (str): The input of the player.
            mode (str):
            roles:
            use:
        Returns:
            dict{}, dict{}
        """
        print(self.player_dict.keys())
        player: Player = self.player_dict[player_name]

        # 与dm交流
        if mode == 0:
            dm_answer = player.talk_to_dm(player_input)
            print('[debug]dm:', dm_answer)
            return dm_answer

        # 与任务演绎系统交流
        elif mode == 1:
            player_use = player.organize_player_use(equipment, skill)
            judge, play = player.talk_to_director(player_input, player_use)
            print('[debug]play:', judge, play)

            # 判断是否出现新人物
            if play["role"] and play["role"] not in roles:
                print("generating img...")
                description = f"【场景】{play['text']}\n【需要描绘的角色】{play['role']}"
                img = self.sd.standard_workflow(description, 1)

                play["npc_data"] = True
                play["image_data"] = img

            # 游戏结束，进入结算
            elif play["status"] == 1:
                task_name = player.takeOffTask()
                self.task_queue.pop(task_name)

                rewards = play["reward"]
                if rewards:
                    player.getReward(rewards)

                play["npc_data"] = False
                play["image_data"] = None

            # 游戏正常进行且没有新角色
            else:
                play["npc_data"] = False
                play["image_data"] = None

            return play

    def select_task(self, player_name: str, task_name: str):
        """
        Args:
            player_name (str): _description_
            task_name (str): _description_

        Returns:
        bool: if the user selected the task.
        """

        print(player_name, task_name)
        task = self.task_queue[task_name]
        play = str(task)

        if task["occupied"]:
            return False, ""
        else:
            task_img = self.sd.standard_workflow(play, 2)

            task["occupied"] = True
            task["player"] = player_name

            judge_prompt = read_file("judge")
            act_prompt = read_file("task_acting")

            judge: LLMAPI = initialize_llm(judge_prompt)
            task_director: LLMAPI = initialize_llm(act_prompt)
            start: str = task_director.generateResponse(play)
            print('start>', start)

            player: Player = self.player_dict[player_name]
            player.takeOnTask(task_director, judge, task_name)

            return start, task_img

    def select_personal_task(self, player_name: str, task_name: str):
        """
        Args:
            player_name (str): _description_
            task_name (str): _description_

        Returns:
        bool: if the user selected the task.
        """

        print(player_name, task_name)
        player: Player = self.player_dict[player_name]
        task = player.personal_task_queue[task_name]
        play = str(task)

        if task["occupied"]:
            return False, ""
        else:
            task_img = self.sd.standard_workflow(play, 2)

            task["occupied"] = True
            task["player"] = player_name

            judge_prompt = read_file("judge")
            act_prompt = read_file("task_acting")

            judge: LLMAPI = initialize_llm(judge_prompt)
            task_director: LLMAPI = initialize_llm(act_prompt)
            start: str = task_director.generateResponse(play)
            print('start>', start)

            player: Player = self.player_dict[player_name]
            player.takeOnTask(task_director, judge, task_name)

            return start, task_img

    def craft_items(self, player_name: str, mode: int, num: int, description: str):
        attribute = self.get_player_info(player_name)
        player: Player = self.player_dict[player_name]

        if description == "":
            return "Error"

        if mode == 0:
            if attribute['凤羽'] < num:
                return "您的凤羽储量不足，请不要为难我，勇士！"
            request = f"{player_name}想要制作{description}的装备，对此玩家愿意投入{num} 凤羽"
            response = self.equipment_generator.generateResponse(request)

            if DEBUG:
                print(response)

            response = fixResponse(response, "outlook")
            response = fixResponse(response, "description")

            equip = json.loads(response)

            player.bag[equip['name']] = equip
            player.consumeProperty('凤羽', num)

            return equip

        elif mode == 1:
            if attribute['龙眼'] < num:
                return "您的龙眼储量不足，请不要为难我，勇士！"
            request = f"【请求之人】{player_name} 需要一个{description}的技能，对此我愿意投入{num}个龙眼。"
            response = self.skill_generator.generateResponse(request)

            if DEBUG:
                print(response)

            skill = json.loads(response)

            response = fixResponse(response, "effect")

            player.bag[skill['name']] = skill
            player.consumeProperty('龙眼', num)

            return skill

    def get_all_available_tasks(self, player_name):
        tasks = [task["task_name"] for task in self.task_queue.values() if task["occupied"] == False]

        return tasks

    def get_all_available_personal_tasks(self, player_name):
        player: Player = self.player_dict[player_name]
        tasks = [task["task_name"] for task in player.personal_task_queue.values()]

        return tasks

    def get_player_info(self, name):
        player: Player = self.player_dict[name]
        print(f"Welcome, {player.name}!")
        return player.attributes


class MultiThreadManager:
    def __init__(self, backend_sys: BackEndSystem, check_interval=600):
        self.backend_sys = backend_sys
        self.check_interval = check_interval

        self.threads = []
        self.running = True

        # 创建并启动任务监控线程
        monitor_thread = threading.Thread(target=self.refresh_task_queue)
        monitor_thread.start()
        self.threads.append(monitor_thread)

        # 创建并启动玩家信息保存线程
        player_thread = threading.Thread(target=self.save_player_info)
        player_thread.start()
        self.threads.append(player_thread)

    # 每隔600秒检查一次任务队列，如果小于3就会自动补充
    def refresh_task_queue(self, max_size=3):
        while self.running:
            existed_task_num = len(self.backend_sys.task_queue)
            if len(self.backend_sys.task_queue) < max_size:
                new_task_num = max_size - existed_task_num
                self.backend_sys.refresh_task_queue(new_task_num)
                print(f"队列大小少于{max_size}，已添加{new_task_num}个元素。当前队列大小：{len(self.backend_sys.task_queue)}")
            time.sleep(self.check_interval)

    def save_player_info(self):
        while self.running:
            for name, info in self.backend_sys.online_player.items():
                filename = f'./saves/{name}.pkl'
                with open(filename, 'wb') as file:
                    pickle.dump(info, file)
            time.sleep(self.check_interval)

    def stop(self):
        self.running = False
        for thread in self.threads:
            thread.join()



