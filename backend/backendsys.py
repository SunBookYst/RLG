import sys
from datetime import datetime
import random
import time
import threading
import pickle
import json
import os
import base64
from typing import Tuple, Dict, List, Any, Callable
from typing import TypeVar,Literal
Base64 = TypeVar('Base64')

sys.path.append('..')

from connection import LLMAPI, StableDiffusion
from connection.llmapi import initialize_llm
from util.constant import INITIAL_DRAGON_EYE, INITIAL_PHONEIX_FEATURE, INITIAL_EXPERIENCE, TASK_DISTRIBUTION, MAX_TASKNUM_QUEUE, REFRESH_TASKQUEUE_INTERVAL_SECONDS,SAVE_USER_INFO_INTERVAL_SECONDS,USER_EXPIRE_TIME,TASK_EXPIRE_TIME,CHECK_OFFLINE_INTERVAL_SECONDS,CHECK_DEAD_BATTLE_INTERVAL_SECONDS,WINNING_ROUND_TO_END
from util.constant import BattleStatus
from util.prompt import (TASK_PROMPT, EQUIPMENT_PROMPT, SKILL_PROMPT, CUSTOM_PROMPT, DM_PROMPT, JUDGE_PROMPT,
                            ACT_PROMPT, BATTLE_PROMPT, SUM_PROMPT_TEMPLATE)

from util.utils import debug_print, fix_response


# debug模式
DEBUG = True
# 全局线程锁
LOCK = threading.Lock()

class Player(object):
    """
    A class to gather all the information of the player.

    Attributes:
    ---
        - name (str): the name of the player.
        - email (str): the email of the player.
        - portrait (base64): the base64 encoded image portrait of the player.
        - password (str): the encrypted password of the player.
        - feature (str): the feature of the player.
        - property (dict): the attributes of the player, including [Dragon Eye], [phoneix feature] and [experiments] so far.
        - personal_task_queue (dict): the personal task queue of the player.
        - bag (dict): the bag of the player, containing all the equipments.
        - skills (dict): the skills of the player, containing all the skills.
        - custom_tasks (list): the custom tasks of the player.

        - dm_model (LLMAPI): The DM LLM assigned to the player.
        - equipment_generator (LLMAPI): The equipment generator LLM assigned to the player.
        - skill_generator (LLMAPI): The skill generator LLM assigned to the player.
        - task_custom (LLMAPI): The task custom LLM assigned to the player.

        - task_focus (bool): whether the player is focusing on a task.
        - current_task (str): the current task the player is focusing on.
        - task_director (LLMAPI): The task director LLM assigned to the player temporarily.
        - task_judge (LLMAPI): The task judge LLM assigned to the player temporarily.

        - current_opponent (str): the current opponent the player is facing when in battle system.
        - challenge_queue (dict{str:dict{str:str|int}}) the battle queue for the player. Goes as
        {
            (str) battle_id: {
                'challenger': (str) challenger_name,
                'target': (str) target_name,
                'status': (int) the status of the battle.
            }
        }

    Methods:
    ---
        - takeTask(task_director, judge, task_name)
        - leaveTask() -> str
        - talkToDM(player_input) -> Dict{str:int|str|None}
        - talkToDirector(player_input, player_use) -> Dict,Dict
        - getReward(reward)
        - checkProperty(item, num) -> bool
        - consumeProperty(item, num) -> bool
        - organizePlayerUse(equipment_list, skill_list) -> dict{str:list[dict[str:Player]]}
    """

    def __init__(self, 
                name: str,
                email: str,
                password: str,
                DM_model: LLMAPI,
                eg_model: LLMAPI,
                sg_model: LLMAPI,
                tc_model: LLMAPI,
                portrait: base64,
                feature:str =  "【苍穹】大陆上的游戏角色，目前是一个健全的人"):

        self.name     : str    = name
        self.email    : str    = email
        self.portrait : base64 = portrait
        self.password : str    = password
        self.feature  : str    = feature
        self.property : dict   = {
            "龙眼"  : INITIAL_DRAGON_EYE,
            "凤羽"  : INITIAL_PHONEIX_FEATURE,
            "经验值": INITIAL_EXPERIENCE,
        }

        # The DM assigned.
        self.dm_model           : LLMAPI = DM_model
        self.equipment_generator: LLMAPI = eg_model
        self.skill_generator    : LLMAPI = sg_model
        self.task_custom        : LLMAPI = tc_model

        self.task_director   : LLMAPI = None
        self.task_judge      : LLMAPI = None
        self.task_focus      : bool = False
        self.current_task    : str = None
        self.current_opponent: str = None

        # 玩家的个性化任务
        self.personal_task_queue: dict = {}
        self.bag                : dict = {}
        self.skills             : dict = {}

        # PVP
        self.challenge_queue: Dict[str,Dict[str, str|int]] = {}

    def takeTask(self, 
                task_director: LLMAPI,
                judge        : LLMAPI,
                task_name    : str):
        """
        Take a task.

        To take a task, the user will be assigned to a director and a judge. furthermore, the user will change the focus to the task, so not to take multiple task at the same time.

        Args:
            task_director (LLMAPI): the LLM to direct the task.
            judge (LLMAPI): the LLM to judge the player's action.
            task_name (str): to indicate which task the player is taking.
        """

        # assign LLM
        self.task_director = task_director
        self.task_judge    = judge
        # change focus
        self.task_focus    = True
        self.current_task  = task_name

    def leaveTask(self) -> str:
        """
        Leave the current task, and make settlements.

        To leave a task, the user will release the LLM assigned to the task, and change the focus back to the DM. The task name will be returned to free the task in task_queue.

        Returns:
            str: the task name.
        """
        # release LLM
        self.task_director = None
        self.task_judge = None
        # change focus
        self.task_focus = False
        task_name = self.current_task
        self.current_task = None

        return task_name

    def talkToDM(self, player_input: str) -> Dict:
        """
        based on the input to generate a response.

        Args:
            player_input (str): the user input.

        Returns:
            dict{}: the response from DM.
            {
                "status": (int [0 | 1]) for the type of the conversation.
                "role": "系统" for role of the conversation.
                "text": (str) for the content of the conversation.
                "task_name": (str|None) if the user is about to take on a task.
            }
        """
        debug_print("conversation with DM")

        response = self.dm_model.generateResponse(f'【玩家】{player_input}')
        debug_print(response)
        response = json.loads(response)

        return response

    def talkToDirector(self, 
                        player_input: str,
                        player_use  : List[Dict[str,str]])->Tuple[dict,dict]:
        """
        
        Talk to the task_director.

        Args:
            player_input (str): the latest input of the player.
            player_use (List[dict{str:str}]): the equipment and skills which the player uses.

        Returns:
            dict{}: the response from judge.
            {
                "judge": (str ["0" | "1"]) for the result of judgement}
                "reason": (str) for the reason of the judgement.
            }
            dict{}: the response from task_director.
            {
                "text": (str) for the description of the task.
                "status": (int [0 / 1]) indicating if the task is over.
                "role": (str) the NPC name who is talking to the player.
                "reward": (dict{str:int}|None) for the reward of the task.
            }
        """

        debug_print("conversation with task")

        system_words = self.task_director.getAllConversation()[-1]["content"]
        player_profile = self.property | {"character": self.feature} | {"use": player_use}

        play_infos = {
            "system": system_words,
            "player": player_input,
            "player_status": player_profile
        }

        # Check if the action is practical.
        content = json.dumps(play_infos, ensure_ascii=False)
        response = self.task_judge.generateResponse(content)
        judge = json.loads(response)

        task_play = {
            "player": player_input,
            "judge" : judge["judge"],
            "reason": judge["reason"]
        }

        # generate response from the director.
        content = json.dumps(task_play, ensure_ascii=False)
        response = self.task_director.generateResponse(content)
        response = fix_response(response, "text")
        play = json.loads(response)

        return judge, play

    def getReward(self, rewards: dict):
        """
        Update the player's property based on the rewards.

        Args:
            rewards (dict): the information of rewards.
        """

        debug_print(rewards)

        if not rewards or rewards == {}:
            return

        for k, v in rewards.items():
            if k in self.property:
                self.property[k] += v
            else:
                debug_print("Not presented attr {k}.")

    def checkProperty(self, item:str, num:int) -> bool:
        """
        Check if the player can afford the property.

        Args:
            item (str): the name of the property.
            num (int): the number of the property.

        Returns:
            bool: whether the player can afford the property.
        """

        return self.property[item] >= num

    def consumeProperty(self, item: str, num: int) -> bool:
        """
        Consume the property of the player.

        Args:
            item (str): the name of the property.
            num (int): the number of the property.

        Returns:
            bool: whether the player can afford the property. If true, then will comsume atomatically.
        """

        if self.property[item] < num:
            return False
        else:
            self.property[item] -= num
            return True

    def organizePlayerUse(self, 
                        equipment_list: list,
                        skill_list    : list) -> List[Dict[str, Dict]]:
        """
        To find the equipment and skill that the player owns.

        Args:
            equipment_list (list)
            skill_list (list)

        Returns:
            dict: the result of the search.
            {
                "equipment": (List[dict]),
                "skill": (list[dict])
            }
        """
        result = {
            "equipment": [self.bag[equip_name] for equip_name in equipment_list],
            "skill": [self.skills[skill_name] for skill_name in skill_list]
        }

        return result



class Battle(object):
    """
    Now I simply could't understand...
    This is a simple implementation for the battle system in the game.

    Attributes:
    ---
    - battle_id (str): The string to identify a battle.
    - create_time (datetime): The time when the battle is created.
    - status (int): The status of the battle.
    - sys (LLMAPI): The LLMAPI object of the battle.
    - challenger(str): The name of the challenger.
    - challenger_role (Player): The role of the challenger.
    - target(str): The name of the target.
    - target_role (Player): The role of the target.
    - pair(dict{str:str}): to get the pair of the battle.
    - roles(dict{str:Player}): Get the Player by str.
    - last_round(dict): The complex idea of the last round.
    {
        (str) challenger_name: (int [0 | 1]) whether to take action.
        (str) target_name: (int [0 | 1]) whether to take action.
        'details': {
            (str) challenger_name: {
                'action': (str) the action text of the challenger.
                'status': (List[str]) the equipment and skills.
                },
            (str) targer_name:{
                'action': (str) the action text of the challenger.
                'status': (List[str]) the equipment and skills.
                }
            'sys': (str) the description of the system.
        }
    }
    - new_round(dict): ... What is this?
    {
        'details': {
            (str) challenger_name: {
                'action': (str) the action text of the challenger.
                'status': (List[str]) the equipment and skills.
            },
            (str) targer_name:{
                'action': (str) the action text of the challenger.
                'status': (List[str]) the equipment and skills.
            },
        }
    - record(dict): sth.

    Methods:
    ---
    - checkResult() -> bool, str|None
    - directFight(player) -> str,bool
    - settleBattle(winner, loser) 
    """
    def __init__(self, 
                player1     : str,
                player2     : str,
                player1_role: Player,
                player2_role: Player,
                battle_id   : str): 

        self.battle_id   : str      = battle_id
        self.create_time : datetime = datetime.now()
        self.status      : int      = BattleStatus.waiting
        self.sys         : LLMAPI   = None

        self.challenger: str = player1
        self.target    : str = player2
        self.challenger_role: Player = player1_role
        self.target_role    : Player = player2_role

        self.roles: Dict[str, Player] = {
            player1: self.challenger_role, 
            player2: self.target_role
        }
        self.pair: dict[str,str] = {
            player1: player2, 
            player2: player1
        }

        # 已经完成的上一回合战斗
        self.last_round: Dict[str,int|Dict[str,Dict[str,str]|str]] = {
            self.challenger: 0,
            self.target    : 0,
            'details': {
                self.challenger: None,
                self.target    : None,
                'sys'          : None
            }
        }
        # 等待完成的新一回合战斗
        self.now_round: Dict[Literal['details'], Dict[str, Dict[str,str]]] = {'details': {}}
        # 得分记录
        self.record: Dict[str,int] = {player1: 0, player2: 0}

    def checkResult(self) -> Tuple[bool, str|None]:
        """
        To check if the battle is over.

        Returns:
            bool: whether the battle is end.
            str|None: if the battle is end, return the winner, else return None
        """

        scores = list(self.record.values())
        if scores[0] == WINNING_ROUND_TO_END:
            return True, self.challenger
        elif scores[1] == WINNING_ROUND_TO_END:
            return True, self.target
        else:
            return False, None

    def directFight(self, player:str) -> Tuple[str, bool]:
        """
        I just could't fix this....

        Called when both players take action.

        Returns:
            str: the result of the fight.
            bool: whether the fight is over.
        """
        debug_print("Fighting.")

        opponent = self.pair[player]
        # player是指触发该方法的player
        details = {
            self.challenger: {
                "action": self.now_round['details'][self.challenger]['action'],
                "status": self.now_round['details'][self.challenger]['status'],
            },
            self.target: {
                "action": self.now_round['details'][self.target]['action'],
                "status": self.now_round['details'][self.target]['status'],
            },
        }
        content = json.dumps(details, ensure_ascii=False)
        res:Dict[Literal["description"]|Literal["judge"], str|Literal["平局"]] = json.loads(self.sys.generateResponse(content))

        debug_print(res)

        if res['judge'] != "平局":
            self.record[res['judge']] += 1

        battle_status = False

        is_end, winner = self.checkResult()
        if is_end:
            battle_status = True
            self.status = BattleStatus.finished

            loser = self.pair[winner]
            self.settleBattle(winner, loser)
            res['description'] += f"【{winner}】赢得了胜利！"
            
        # To absurd to do this...
        self.last_round = self.now_round
        self.last_round['details']['sys'] = res["description"]
        self.last_round[player] = 1             # 已阅
        self.last_round[self.pair[player]] = 0  # 未读

        self.now_round = {'details': {}}

        return res['description'], battle_status

    def settleBattle(self, winner:str, loser:str):
        """
        To settle the battle, and give rewards to both sides.

        Args:
            winner (str):
            loser (str):
        """
        prompt = SUM_PROMPT_TEMPLATE.format(winner=winner, loser=loser)
        res = json.loads(self.sys.generateResponse(prompt))
        self.roles[winner].getReward(res[winner])
        self.roles[loser].getReward(res[loser])


class BackEndSystem(object):
    """
    The backend system of the game, mainly maintain the critical information of the game.
    Or really if so...

    Attributes:
    ---
        - task_generator (LLMAPI): the overall task generator.
        - sd (StableDiffusion): The model to generate avatars and backgrounds.
        - task_queue (dict{}) the task information.
        - battle_queue (dict{}) The battle queue information.

        - player_dict (dict{str:Player}): all the registered players.
        - player_dict2 (dict{str:Player}): all the players indexed by email.
        - online_player (dict{str:datetime}): all the online players.


    Methods:
    ---
        - registerPlayer(name,email,password,portrait)->bool
        - loginPlayer(email,password) -> str|None
        - updateTaskQueue(supply_num)
        - taskGenerate(task_type, description) -> dict
        - taskCustomize(player_name, description) -> dict
        - getPlayerInput(player_name, player_input, mode, equipment, skill, roles) -> dict{str:Any}
        - selectTask(player_name, task_name, mode) -> dict
        - getPlayerProperty(name) -> dict{str:int}
        - craftItems(player_name, mode, num, description) -> str|dict
        - getAllAvailableTasks() -> list[str]
        - getAllAvailablePersonalTasks(player_name) -> list[str]
        - getAllAvailablePublicTasks() -> list[str]
        - getAllOnlinePlayers() -> List[str], List[base64]
        - createBattle(player1, player2) -> str
        - acceptBattle(player, battle_id) -> int
        - rejectBattle(player, battle_id) -> int
        - playerBattle(player, battle_id) -> str,str,str,bool
        - getOnlinePlayers() -> list[str]
        - onlineConfirm(player)
        - getChallengeList(player)
    """

    def __init__(self):

        self.name2player_dict  : Dict[str,Player]   = {}
        self.email2player_dict : Dict[str,Player]   = {}
        self.online_player     : Dict[str,datetime] = {}

        # 各组件初始化
        self.task_generator: LLMAPI = initialize_llm(TASK_PROMPT)

        # Why doing so?
        # sd内部有llm
        self.sd: StableDiffusion = StableDiffusion()
        # self.sd.initialize()

        # 任务队列
        self.task_queue:Dict[str,Dict] = {}

        # 战斗队列
        self.battle_queue: Dict[str,Battle] = {}

    def registerPlayer(self, 
                        name    : str,
                        email   : str,
                        password: str,
                        portrait: base64) -> bool: 
        """
        Add a new instance of Player in the DM.
        The name and the feature are firstly checked.

        TODO: Fully use the email and whatsoever.

        Args:
            name (str): The player name.
            email (str): The player email.
            password (str): The player password.
            portrait (base64): The player image.

        Returns:
            bool: True if the registration is successful.
        """

        if name in self.name2player_dict:
            return False
        if email in self.email2player_dict:
            return False

        dm_model           : LLMAPI = initialize_llm(DM_PROMPT)
        equipment_generator: LLMAPI = initialize_llm(EQUIPMENT_PROMPT)
        skill_generator    : LLMAPI = initialize_llm(SKILL_PROMPT)
        task_custom        : LLMAPI = initialize_llm(CUSTOM_PROMPT)

        new_player: Player = Player(name, email, password, dm_model, equipment_generator, skill_generator, task_custom, portrait)

        with LOCK:
            # regist the user in the list.
            self.name2player_dict[name] = new_player
            self.email2player_dict[email] = new_player
            self.online_player[name] = new_player

        return True

    def loginPlayer(self,
                    email   : str,
                    password: str) -> str|None: 
        """
        Login the player by using email and password.

        Args:
            email (str): the email to indentify the player.
            password (str): the password to indentify the player.

        Returns:
            str|None: the player'name if login successfully, or none if failed.
        """
        if email not in self.email2player_dict.keys():
            return None

        player: Player = self.email2player_dict[email]

        if password != player.password:
            return None

        with LOCK:
            self.online_player[player.name] = datetime.now()
        return player.name

    def updateTaskQueue(self, supply_num:int):
        """
        Check and update the task queue, making the queue is full.

        Args:
            supply_num (int): the number of tasks to be added.
        """
        task_type    :List[str]   = list(TASK_DISTRIBUTION.keys())
        probabilities:List[float] = list(TASK_DISTRIBUTION.values())
        for __ in range(supply_num):
            chosen_item = random.choices(task_type, weights=probabilities, k=1)[0]
            task = self.taskGenerate(chosen_item)
            self.task_queue[task["task_name"]] = task

    def taskGenerate(self, 
                    task_type  : str,
                    description: str = "任意") -> Dict[str,str|Dict|bool|None]: 
        """
        Generate a task based on the task type and description.

        Args:
            task_generator (LLMAPI): The task generator.
            task_type (str): the type of the task
            description (str, optional): The detailed description of the task. Defaults to "任意".

        Returns:
            dict{}: The information of generated task.
            {
                "task_name": (str) the name of the task.
                "task_description": (str) the desc of the task. 
                "attention": (str) the precautions of the task.
                "reward": (dict{str:int}) the reward for finishing the task.
                "occupied": False, whether the task is occupied.
                "player": None, the player name who is occuping the task.
            }
        """
        need = f"帮我生成一个{description}的{task_type}"
        task = self.task_generator.generateResponse(need)
        task = json.loads(task)
        task["occupied"] = False
        task["player"] = None
        return task

    def taskCustomize(self, 
                    player_name: str, 
                    description: str = "任意") -> Dict[str,str|Dict|bool|None]:
        """
        Customize the task based on the description. Note that this task is private and not visible for other players.

        Args:
            player_name (str): the player name who asking the task.
            description (str, optional): the description of the task. Defaults to "任意".

        Returns:
            dict: the customized task information.
        """
        player: Player = self.name2player_dict[player_name]

        need = f"【玩家】帮我生成一个任务， 要求是{description}"
        task = player.task_custom.generateResponse(need)
        task = json.loads(task)

        player.personal_task_queue[task['task_name']] = task

        return task

    def getPlayerInput(self, 
                        player_name : str,
                        player_input: str,
                        mode        : int,
                        equipment   : List[Dict] = [],
                        skill       : List[Dict] = [],
                        roles       : List[str]  = []) -> Dict[str, Any]:
        """
        Get the player input and return the response from the system, including the dm and the director.

        Args:
            player_name (str): The name of the player.
            player_input (str): The input of the player.
            mode (int): the code to indicate the mode of the system. 
            0: Talking to DM.
            1: Talking to director.
            equipment (list, optional): The equipment of the player. Defaults to [].
            skill (list, optional): The skill of the player. Defaults to [].
            roles (list, optional): The previous NPCs appeared. Defaults to [].
        
        Returns:
            dict{}: the result from DM or director.
            mode == 0:
            {
                "status": (int [0 | 1]) for the type of the conversation.
                "role": "系统" for role of the conversation.
                "text": (str) for the content of the conversation.
                "task_name": (str|None) if the user is about to take on a task
            }
            mode == 1:
            {
                "text": (str) for the description of the task.
                "status": (int [0 / 1]) indicating if the task is over.
                "role": (str) the NPC name who is talking to the player.
                "reward": (dict{str:int}|None) for the reward of the task.
            }

        Raises:
            ValueError: If the player is not found.

        """
        # debug_print(self.name2player_dict.keys())
        if player_name not in self.name2player_dict.keys():
            raise ValueError("Player not found")
        player: Player = self.name2player_dict.get(player_name)

        match mode:
            case 0:
                return player.talkToDM(player_input)
            case 1:
                # As you wish.
                player_use = player.organizePlayerUse(equipment, skill)
                judge, play = player.talkToDirector(player_input, player_use)
                # debug_print('[debug]play:', judge, play)

                # Check if a new NPC appears. Say, generate a new NPC image.
                if play["role"] and play["role"] not in roles:
                    debug_print("generating img...")
                    description = f"【场景】{play['text']}\n【需要描绘的角色】{play['role']}"
                    img = self.sd.standard_workflow(description, 1)
                    play["image_data"] = img

                # The end of the task, settle for rewards.
                elif play["status"] == 1:
                    task_name = player.leaveTask()
                    self.task_queue.pop(task_name)

                    rewards = play["reward"]
                    if rewards:
                        player.getReward(rewards)
                    play["image_data"] = None

                # The task normally process without meeting new NPC.
                else:
                    play["image_data"] = None

                return play

    def selectTask(self, 
                    player_name: str,
                    task_name  : str,
                    mode       : int) -> Dict[str, str|int|None]: 
        """
        Args:
            player_name (str): the player's name who chose the task.
            task_name (str): the task's name which is chosen.
            mode (int): public task(0) or personal task(1)

        Returns:
            dict{}: the initial_scene generated by the director.
            {
                "text": (str) the initial description of the task.
                "status": 0, the task is not over.
                "role": None, the system is saying.
                "image_data": (base64): the background image of the task.
            }

        Raises:
            ValueError: when the task is not avaliable.
        """
        debug_print(player_name, task_name)
        player: Player = self.name2player_dict.get(player_name)

        match mode:
            case 0:
                task = self.task_queue.get(task_name)
            case 1:
                task = player.personal_task_queue[task_name]

        play = json.dumps(task)
        task_img = self.sd.standard_workflow(play, 2)

        with LOCK:
            task["occupied"] = True
            task["player"]   = player_name

        judge        : LLMAPI = initialize_llm(JUDGE_PROMPT)
        task_director: LLMAPI = initialize_llm(ACT_PROMPT)

        initial_scene = task_director.generateResponse(play)
        initial_scene = json.loads(initial_scene)
        initial_scene['image_data'] = task_img

        debug_print('start>', initial_scene)

        player.takeTask(task_director, judge, task_name)

        return initial_scene

    def getPlayerProperty(self, name) -> Dict[str,int]|None:
        """
        this returns the propoerty of the player.

        Args:
            name (str): the name of the player.

        Returns:
            dict{str:int}|None: the property of the player.
            {
                "龙眼": (int) the number of Dragon Eyes the player has.
                "凤羽": (int) the number of Phoenix Feathers the player has.
                "经验值": (int) the number of Experience the player has.
            }
        """
        if name in self.name2player_dict.keys():
            player: Player = self.name2player_dict.get(name)
            return player.property
        else:
            return None

    def craftItems(self, 
                    player_name: str,
                    mode       : int,
                    num        : int,
                    description: str) -> str|Dict[str,str|int]: 
        """
        Either craft equipment or skill, function will register the result, and consume the property.

        Args:
            player_name (str): the player who is about to craft.
            mode (int): 0 for equipment, 1 for skill.
            num (int): the number of resources the player is willing to use.
            description (str): the description of the expected item.

        Returns:
            str|dict: Neither the information of why failed, or the real information dict for equipment/skill

        Raises:
            ValueError: when the player could not found.
        """
        if player_name not in self.name2player_dict.keys():
            raise ValueError("The player is not registered")
        
        player: Player = self.name2player_dict.get(player_name)

        if description == "":
            return "Error"

        if mode == 0:
            if not player.checkProperty('凤羽', num):
                return "您的凤羽储量不足，请不要为难我，勇士！"
            
            request = f"{player_name}想要制作{description}的装备，对此玩家愿意投入 {num} 凤羽"
            response = player.equipment_generator.generateResponse(request)

            debug_print(response)

            response = fix_response(response, "outlook")
            response = fix_response(response, "description")
            equip = json.loads(response)
            player.bag[equip['name']] = equip
            player.consumeProperty('凤羽', num)
            return equip

        elif mode == 1:
            if not player.checkProperty('龙眼', num):
                return "您的龙眼储量不足，请不要为难我，勇士！"
            
            request = f"【请求之人】{player_name} 需要一个{description}的技能，对此我愿意投入{num}个龙眼。"
            response = player.skill_generator.generateResponse(request)

            debug_print(response)

            skill = json.loads(fix_response(response, "effect"))
            player.skills[skill['name']] = skill

            player.consumeProperty('龙眼', num)

            return skill
        
        else:
            raise ValueError("Unknown mode to craft items.")

    def getAllAvailableTasks(self) -> List[str]:
        """
        Return all the tasks that are available for public.

        Returns:
            List[str]: the result.
        """
        tasks = [task["task_name"] for task in self.task_queue.values() if task["occupied"] is False]

        return tasks

    def getAllAvailablePersonalTasks(self, player_name) -> List[str]:
        """
        return all the tasks that are private, and also not occupied...

        Args:
            player_name (str): the player name...

        Returns:
            List[str]: the result.
        """
        player: Player = self.name2player_dict[player_name]
        tasks = [task["task_name"] for task in player.personal_task_queue.values()]

        return tasks
    
    def getAllOnlinePlayers(self) -> Tuple[List[str], List[Base64]]:
        """
        Return all the online players.

        TODO: well actually this may fix as List[Dict[str:base64]]

        Returns:
            List[str]: All the online players' name.
            List[Base64]: All the online players' portrait.
        """

        name_list = []
        image_list = []
        for player_name in self.online_player.keys():
            name_list.append(player_name)
            image_list.append(self.name2player_dict.get(player_name).portrait)
        return name_list, image_list

    def createBattle(self, 
                    player1: str, 
                    player2: str) -> str:
        """
        Create a battle between two players.

        Args:
            player1 (str): the name of the player_1
            player2 (str): the name of the player_2

        Returns:
            str: the string to identify the battle.
        """
        battle_id = player1 + player2
        player_role1: Player = self.name2player_dict[player1]
        player_role2: Player = self.name2player_dict[player2]

        # ? ...
        new_battle: Battle = Battle(player1, player2, player_role1, player_role2, battle_id)

        # Append the battle to the battle queue.
        with LOCK:
            self.battle_queue[battle_id] = new_battle

        # update the two player's challange_queue
        player_role1.challenge_queue[battle_id] = {
            'challenger': player1,
            'target'    : player2,
            'status'    : 0
        }
        player_role2.challenge_queue[battle_id] = {
            'challenger': player1,
            'target'    : player2,
            'status'    : 0
        }
        return battle_id

    def acceptBattle(self, player, battle_id:str) -> int:
        """
        Called when the player accept the task.

        Args:
            player (str): ... Why to user?
            battle_id (str): the battle id. 

        Returns:
            int: (200 | 404) the status code of the result.
        """
        try:
            with LOCK:
                battle_sys: LLMAPI = initialize_llm(BATTLE_PROMPT)

                if battle_id not in self.battle_queue.keys():
                    return 404
                
                battle = self.battle_queue.get(battle_id)
                battle.status = BattleStatus.accept
                battle.sys = battle_sys

                battle.challenger_role.challenge_queue[battle_id]['status'] = 1
                battle.target_role.challenge_queue[battle_id]['status'] = 1
            return 200
        
        except:
            return 404

    def rejectBattle(self, 
                    player, 
                    battle_id:str):
        """
        Called when the player reject the task.

        Why don't combine the two functions...

        Args:
            player (Any): Not used clearly.
            battle_id (str): the battle id.

        Returns:
            int: [200 | 400] the result for rejecting the task.
        """
        try:
            if battle_id not in self.battle_queue.keys():
                return 404
            
            battle: Battle = self.battle_queue.get(battle_id)
            with LOCK:
                battle.status = BattleStatus.refuse
                self.battle_queue.pop(battle_id)

            battle.challenger_role.challenge_queue.pop(battle_id)
            battle.target_role.challenge_queue.pop(battle_id)
            return 200
        
        except:
            return 404

    def playerBattle(self, 
                    battle_id   : str,
                    player      : str,
                    player_input: str,
                    equipment   : List[Dict[str,str]],
                    skill       : List[Dict[str,str]]) -> Tuple[str,str,str, bool]: 
        """
        Called when the player take actions.

        The returns are too frustrating.

        Args:
            battle_id (str): the id.
            player (str): the player's name
            player_input (str): the player's input
            equipment (List[Dict[str,str]]): the equipment the player used
            skill (List[Dict[str,str]]): the skill the player used

        Returns:
            str: The opponent's name
            str: The opponent's action
            str: The description of the battle
            bool: The result of the battle (if ended.)
        """

        player_role: Player = self.name2player_dict[player]
        battle     : Battle = self.battle_queue[battle_id]
        battle_status = False

        player_status = player_role.organizePlayerUse(equipment, skill)

        with LOCK:
            debug_print(f"player {player} has input!")
            debug_print(f"battle_id: {id(battle)}")

            # Update the detail part for the player of now_round 
            battle.now_round['details'][player] = {
                'action': player_input, 
                'status': player_status
            }

            debug_print(battle.now_round)

            opponent = battle.pair[player]

            # if the player is the backhand player.
            if opponent in battle.now_round['details']:
                fight = battle.now_round['details']
                des, battle_status = battle.directFight(player)

                debug_print('successful round!')
                debug_print(f"{opponent},{fight[opponent]},{des},{battle_status}")

                return opponent, fight[opponent]['action'], des, battle_status

            return opponent, "正在出招", "请耐心等待对手", battle_status

    def getOnlinePlayers(self) -> List[str]:
        """
        Get the names of the online players.

        Returns:
            list[str]: the names of the online players.
        """
        return list(self.online_player.keys())

    def onlineConfirm(self, player: str):
        """
        Update the online time for the player. i.e. ensure the player is online.

        Args:
            player (str): the player' name
        """
        with LOCK:
            self.online_player[player] = datetime.now()

    def getChallengeList(self, player: str) -> Tuple[List[str], List[str], List[str]]:
        """
        get the list?

        Args:
            player (str): the player's name

        Returns:
            list[str]: the battle id for battles requiring response.
            list[str]: the opponent's name for battles requiring response.
            list[str]: the battle id for battles accepted.
        """
        player_role: Player = self.name2player_dict[player]
        
        # The list for others challenging me.
        id_list  :List[str] = []
        role_list:List[str] = []
        # The list for me to challenge others, and is accepted.
        accept_id:list[str] = []

        try:
            for battle_id, battle_info in player_role.challenge_queue.items():
                # Not answered.
                if battle_info['target'] == player and battle_info['status'] == 0:
                    id_list.append(battle_id)
                    role_list.append(battle_info['challenger'])

                # as challenger, not accepted.
                if battle_info['status'] == 1 and battle_info['challenger'] == player:
                    with LOCK:
                        player_role.challenge_queue[battle_id]['status'] = BattleStatus.progressing
                    accept_id.append(battle_id)
        except:
            pass
        return id_list, role_list, accept_id

    def getBattleInfo(self, 
                    player: str, 
                    battle_id: str) -> Tuple[str|None, str|None, str|None, bool]:
        """
        Get the information of the battle.

        Args:
            player (str): the player's name
            battle_id (str): the battle id.

        ? It really is confusing enough...

        Returns:
            str|None: the opponent's name.
            str|None: the action of the opponent.
            str|None: the description of the system.
            bool: whether the battle is over.
        """

        ending_status = False

        try:
            battle: Battle = self.battle_queue[battle_id]
            if battle.status == BattleStatus.finished or battle.status == BattleStatus.unexpected:
                ending_status = True
            if battle.last_round[player] == 0:
                battle.last_round[player] = 1
                return (battle.pair[player],
                        battle.last_round['details'][battle.pair[player]]['action'],
                        battle.last_round['details']['sys'],
                        ending_status)
            else:
                return None, None, None, ending_status

        except:
            return None, None, None, ending_status


# 负责管理后台系统
class MultiThreadManager:
    """
    This class is used to handle multi-threading.
    """
    def __init__(self, backend_sys: BackEndSystem):
        self.backend_sys: BackEndSystem = backend_sys

        self.threads_pool:List[threading.Thread] = []
        self.running = True
        self.lock = threading.Lock()

        # Create and listen to the task_queue, auto-fill if the queue is not full.
        self.create_and_start_thread(self.refresh_task_queue, "TaskQueueMonitorThread")

        # Create and save data of players at regular time.
        self.create_and_start_thread(self.save_player_info, "PlayerInfoSaveThread")

        # Create and listen to the offline player clear thread.
        self.create_and_start_thread(self.clear_offline_players, "OfflinePlayerClearThread")

        # Create and listen to the dead player clear thread.
        self.create_and_start_thread(self.clear_disabled_battle, "BattleQueueClearThread")

    def create_and_start_thread(self, 
                                target:Callable, 
                                name:str):
        thread = threading.Thread(target=target, name=name)
        thread.start()
        self.threads_pool.append(thread)

    def refresh_task_queue(self):
        """
        Check the task queue, and if the queue is not full, fill the queue to max_size given in constant.
        """
        while self.running:
            try:
                existed_task_num = len(self.backend_sys.task_queue)
                if existed_task_num < MAX_TASKNUM_QUEUE:
                    new_task_num = MAX_TASKNUM_QUEUE - existed_task_num
                    self.backend_sys.updateTaskQueue(new_task_num)
                    debug_print(
                        f"The number of public tasks is less than {MAX_TASKNUM_QUEUE}, {new_task_num} task(s) have been added in the queue。The current size of the queue is{len(self.backend_sys.task_queue)}.")
            except Exception as e:
                print(f"Error in refresh_task_queue: {e}")

            time.sleep(REFRESH_TASKQUEUE_INTERVAL_SECONDS)

    def save_player_info(self):
        """
        To save the player info at regular time.

        ! Hint: the save is stored in a relative path './saves', so please check the running path of the program to find the data.
        """
        while self.running:
            try:
                if not os.path.isdir('./saves'):
                    os.makedirs('./saves')

                auto_save_num = 0
                for name in self.backend_sys.online_player.keys():
                    filename = f'./saves/{name}.pkl'
                    with open(filename, 'wb') as file:
                        pickle.dump(self.backend_sys.name2player_dict[name], file)
                    auto_save_num += 1

                debug_print(f"{auto_save_num} online player(s)' information is successfully saved.")

            except Exception as e:
                print(f"Error in save_player_info: {e}")
            time.sleep(SAVE_USER_INFO_INTERVAL_SECONDS)

    def clear_offline_players(self):
        """
        Clear the queue away from offline players.
        """
        while self.running:
            try:
                online_players = list(self.backend_sys.online_player.keys())
                time_now = datetime.now()
                for name in online_players:
                    if time_now - self.backend_sys.online_player[name] > USER_EXPIRE_TIME:
                        with self.lock:
                            last_time = self.backend_sys.online_player.pop(name)

                        player: Player = self.backend_sys.name2player_dict[name]
                        # Fix battle related.
                        for battle_id in player.challenge_queue.keys():
                            battle: Battle = self.backend_sys.battle_queue[battle_id]
                            battle.last_round['details']['sys'] = f"玩家【{name}】逃跑了。"
                            battle.status = BattleStatus.unexpected

                        if not os.path.isdir('./saves'):
                            os.makedirs('./saves')
                        filename = f'./saves/{name}.pkl'
                        with open(filename, 'wb') as file:
                            pickle.dump(self.backend_sys.name2player_dict[name], file)
                        print(f"玩家 【{name}】 下线了. 最近一次在线时间为: {last_time}")
            except Exception as e:
                print(f"Error in clear_offline_players: {e}")
            time.sleep(CHECK_OFFLINE_INTERVAL_SECONDS)

    def clear_disabled_battle(self):
        """
        Clear battles which is not active.
        """

        def isAbnormallyEnds(battle:Battle):
            return battle.status == BattleStatus.unexpected
        
        def isHangingLong(battle:Battle):
            return battle.status == BattleStatus.waiting and \
                    datetime.now() - battle.create_time > TASK_EXPIRE_TIME

        while self.running:
            try:
                existing_battle = list(self.backend_sys.battle_queue.keys())
                for battle_id in existing_battle:

                    battle = self.backend_sys.battle_queue[battle_id]
                    if isHangingLong(battle) or isAbnormallyEnds(battle):

                        moved_battle: Battle = self.backend_sys.battle_queue.pop(battle_id)

                        moved_battle.challenger_role.challenge_queue.pop(battle_id)
                        moved_battle.target_role.challenge_queue.pop(battle_id)
                        print(f"移除了战斗 “{battle_id}”, 发起时间为{moved_battle.create_time}")
                        del moved_battle  # 显式删除引用

            except Exception as e:
                print(f"Error in clear_rejected_battle: {e}")
            time.sleep(CHECK_DEAD_BATTLE_INTERVAL_SECONDS)

    def stop(self):
        self.running = False
        for thread in self.threads_pool:
            thread.join()