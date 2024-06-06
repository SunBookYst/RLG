import sys
sys.path.append('..')

import time
import pickle
from datetime import datetime, timedelta

from utils import *
from request import LLMAPI, StableDiffusion

DEBUG = True

def fixResponse(origin_text:str, attr:str):

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

    def __init__(self, 
                name    : str,
                feature : str,
                DM_model: LLMAPI): 
        
        self.name          :str    = name
        self.feature       :str    = feature
        self.attributes    :dict   = {
            "龙眼": 0,
            "凤羽": 0,
            "经验值": 0,
            "等级": 1
        }
        # 凤羽/龙眼/  level Exp

        self.dm_model      :LLMAPI = DM_model
        self.task_director :LLMAPI = None
        self.task_judge    :LLMAPI = None
        self.task_focus    :bool   = False
        self.current_task  :str    = None
        self.bag   :list = []
        self.skills:list = []

    def takeOnTask(self, task_director, judge, task_name):
        self.task_focus    = True
        self.task_director = task_director
        self.task_judge    = judge
        self.current_task  = task_name

    def takeOffTask(self):
        self.task_focus    = False
        self.task_director = None
        self.task_judge    = None
        task_name = self.current_task
        self.current_task  = None
        return task_name

    def makeAConversation(self, player_input:str):
        """
        based on the input to generate a response.

        Args:
            player_input (str): the user input.

        Returns:
            dict{}: the response from DM/judge
            dict{}/empty dict: The response from the task generator if the user is on task.
        """

        if not self.task_focus:
            if DEBUG:
                print("conversation with DM")
            return json.loads(self.dm_model.generateResponse(f'【玩家】{player_input}')), {}
        
        else:
            if DEBUG:
                print("conversation with task")
            play_infos = {}
            system_words = self.task_director.getAllConversation()[-1]["content"]
            play_infos["system"] = system_words
            play_infos["player"] = player_input
            play_infos["player_status"] = self.attributes

            content = json.dumps(play_infos)

            response = self.task_judge.generateResponse(content)
            print('[jduge]\n',response)
            judge = json.loads(response)
            print('=' * 10)

            task_play = {}
            task_play["player"] = player_input
            task_play["status"] = judge["judge"]
            task_play["reason"] = judge["reason"]

            content = json.dumps(task_play)

            response = self.task_director.generateResponse(content)

            response = fixResponse(response, "text")
            print('[task]\n',response)
            with open("./debug.txt","w",encoding='utf-8') as f:
                f.write(response)
            print('=' * 10)
            play = json.loads(response)
            # play = json.loads(self.task_director.generateResponse(content))

            return judge, play


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

    def __init__(self, one_day_length_minutes = 40):
        """

        Args:
            one_day_length_minutes (int, optional): How long a day in the game in minutes. Defaults to 40.
        """

        task_prompt = read_file("task")
        bg_prompt = read_file('txt2img_background')
        eq_prompt = read_file('equipment_craft')
        sk_prompt = read_file('skill_generate')

        self.player_dict:dict[str:Player] = {}

        self.task_generator      :LLMAPI          = initialize_llm(task_prompt)
        self.bg_generator        :LLMAPI          = initialize_llm(bg_prompt)
        self.sd                  :StableDiffusion = StableDiffusion()
        self.equipment_generator:LLMAPI           = initialize_llm(eq_prompt)
        self.skill_generator     :LLMAPI          = initialize_llm(sk_prompt)

        self.task_queue = {}

        template_task = [self._task_generate("互动任务") for __ in range(4)]

        for t in template_task:
            self.task_queue[t["task_name"]] = t
        # Randomly generate some task. Add attributes: occupied/player.

        self.start_time = datetime.now()

        # self.task_generator=None
        # self.bg_generator=None
        # self.sd=None

        # self._quest_list= {}
        # self._sub_model_dict={}

        # self._pl_data={}

        # self.time_set = one_day_length_minutes

        # self.current_system = 'Main'

        # self.is_playing = False
        
        # self.total_played_time = 0

    def _task_generate(self, task_type, description="任意"):
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


    # Some annoying things from log in.
    def checkNameValid(self, name):
        player_name_lists = self.player_dict.keys()

        valid = name in player_name_lists

        if valid == False:
            self.registerPlayer(name, "")
            return True
        else:
            return False
    
    def checkFeatureValid(self, feature):
        return True

    def registerPlayer(self, name, feature):
        """
        Add a new instance of Player in the DM.
        The name and the feature is first checked.
        
        Args:
            name (str): The player name.
            feature (str): The player's description.
        """

        dm_prompt = read_file("DM")
        dm_model:LLMAPI = initialize_llm(dm_prompt)
        new_player = Player(name, feature, dm_model)

        self.player_dict[name] = new_player

    def getPlayerInput(self, player_name:str, player_input:str):
        """
        Get the player input and return the response from the DM.
        
        Args:
            player_name (str): The name of the player.
            player_input (str): The input of the player.
        
        Returns:
            dict{}, dict{}
        """

        player:Player = self.player_dict[player_name]
        response1, response2 = player.makeAConversation(player_input)

        # print(player.task_focus, response1["status"])
        # print(player.task_focus == False , response1["status"] == 1)

        if player.task_focus == False and response1["status"] == '1':
            print("Changing scene.")
            selected, initial_state = self.selectTask(player_name, response1["task_name"], play = str(self.task_queue[response1["task_name"]]))

            print(selected, '>',initial_state)

            if selected:
                task = self.task_queue[response1["task_name"]]
                response1["status"] = 1
                response1["text"] = initial_state
                response1["sub_img"] = self.sd.generate_background(str(task))
            else:
                response1["status"] = 0
                response1["text"] = "该任务已经被其他人选中"
                response1["sub_img"] = None

        if response2 != {}:
            if response2["status"] == '1':
                task_name = player.takeOffTask()
                self.task_queue.pop(task_name)
                # self.task_queue.pop(task)
                # self.task_queue.pop(task_id)
        return response1, response2
    
    
    def selectTask(self, player_name:str, task_name:str, play = ""):
        """
        Args:
            player_name (str): _description_
            task_name (str): _description_

        Returns:
        bool: if the user selected the task.
        """

        print(player_name, task_name)

        task = self.task_queue[task_name]

        if task["occupied"]:
            return False, ""
        else:
            task["occupied"] = True
            task["player"] = player_name

            judge_prompt = read_file("judge")
            act_prompt = read_file("task_acting")

            judge        :LLMAPI = initialize_llm(judge_prompt)
            task_director:LLMAPI = initialize_llm(act_prompt)
            start        :str    = task_director.generateResponse(play)
            print('start>',start)

            player = self.player_dict[player_name]
            player.takeOnTask(task_director, judge, task_name)

            return True, start
        

    def craft_items(self,
                    player_name:str,
                    mode:int,
                    num:int,
                    description:str):
        if mode == 0:
            request = f"{player_name}想要制作{description}的装备，对此玩家愿意投入{num} 凤羽"

            return json.loads(self.equipment_generator.generateResponse(request))
        
        elif mode == 1:
            request = f"【请求之人】{player_name} 需要一个{description}的技能，对此我愿意投入{num}个龙眼。"

            return json.loads(self.skill_generator.generateResponse(request))


    def getAllAvailableTasks(self, player_name):
        tasks = [task["task_name"] for task in self.task_queue.values() if task["occupied"] == False]
        return tasks
    
    def getPlayerInfo(self, player_name):
        player = self.player_dict[player_name]
        return player.attributes
    
    def getGameTime(self,player_name):
        return "00:00:00"
    

if __name__ == '__main__':

    bs = BackEndSystem()

    # print("Complt.")

    player_name = "RLG"
    player_feature = "我是一个骑士，我有一个大剑，也有一个盾牌，我遵循骑士道义，惩恶扬善，不惧权贵，打抱不平，云游四方，为正义而战，为弱小者而发声。"

    # print("So what?")

    bs.registerPlayer(player_name, player_feature)

    xx = bs.getAllAvailableTasks(player_name)

    print(xx)

    while True:
        user_input = input("Input:")
        response1, response2 = bs.getPlayerInput(player_name, user_input)
        print(response1)
        print(response2)






