import time
import pickle
from datetime import datetime, timedelta
from RLG.Request.llmapi import LLMAPI
from RLG.subsenario.task_genrate import task_generate

class backend(object):
    '''
    后台系统类
        包含属性
        bg:背景信息
        _quest_list:存储任务的字典(任务名:任务信息)
        _sub_model_dict:存储子模型的字典(模型名:模型)
        _pl_data:存储玩家信息的字典(玩家名:玩家信息)
        time_set:时间流速,每多少分钟过去一天
        游戏状态和时间管理:
        self.is_playing :是否在进行游戏
        self.start_time :本次开始记录时间
        self.total_played_time :以往经过时间
        current_system:记录当前活跃的系统,即掌握控制权的系统
        debug:是否打印相关信息
        包含方法
        trans_control:将控制权移交给[sys_name]系统
        get_game_time:获取游戏时间
    '''
    def __init__(self,bg,time_set=40,debug=False):
        '''
        :param bg:给主系统的prompt
        :param time_set: 时间流苏,每多少分钟过去一天
        :param debug: 是否打印信息 Default:False
        '''
        # 背景信息
        self.bg=bg
        # 任务列表
        self._quest_list= {}
        # 已有模型列表
        self._sub_model_dict={}
        # 玩家信息(包括技能\道具等)
        self._pl_data={}
        # 游戏时间设置:多少分钟一天 default:40
        self.time_set=time_set
        # 当前活跃的系统 default:Main
        self.current_system='Main'
        # 是否打印信息, default=False
        self.debug:bool=debug
        # 游戏状态和时间管理
        self.is_playing = False
        self.start_time = None
        self.total_played_time = 0

    def trans_control(self,sys_name):
        '''
        转交控制权
        :param sys_name:
        :return:
        '''
        if sys_name not in self._sub_model_dict:
            if self.debug:
                print(f'fail to transfer control from {self.current_system} to {sys_name}\n{sys_name} not recognized')
            return
        if self.debug:
            print(f"Transferring control from {self.current_system} to {sys_name}")
        # TODO: 给出玩家信息
        self.current_system=sys_name

    def start_game(self):
        '''
        开始游戏时间流逝
        :return: None
        '''
        if not self.is_playing:
            self.is_playing = True
            self.start_time = time.time()
            print("Game started.")

    def pause_game(self):
        '''
        暂停游戏时间流逝
        :return: None
        '''
        if self.is_playing:
            self.is_playing = False
            elapsed_time = time.time() - self.start_time
            self.total_played_time += elapsed_time
            self.start_time = None
            print("Game paused.")

    def get_game_time(self):
        '''
        获取当前的游戏内时间，精确到分钟
        :return: 当前的游戏内时间，字符串格式
        '''
        if self.is_playing:
            elapsed_time = time.time() - self.start_time
            total_elapsed_time = self.total_played_time + elapsed_time
        else:
            total_elapsed_time = self.total_played_time

        # 过去的游戏内时间，分钟
        elapsed_game_minutes = total_elapsed_time / 60 * (1440 / self.time_set)
        # 起始游戏时间（假设游戏从第1天开始）
        game_start_time = datetime(1, 1, 1)
        # 当前游戏内时间
        current_game_time = game_start_time + timedelta(minutes=elapsed_game_minutes)
        return current_game_time.strftime("%Y-%m-%d %H:%M")
    def chat(self,data):
        '''
        与当前活跃的系统对话
        :return:
        '''
        text=data.get('text','')
        user=data.get('user','玩家')
        if self.debug:
            print(f"generate response from {self.current_system},text:{text}")

        #TODO: 用一个工具函数判断玩家需求.接任务/对话 接任务-accept
        if ():
            self.accept(task_name)
            #TODO: 用工具,把信息,调用的系统传给工具函数进行对话
            llm:LLMAPI=self._sub_model_dict[self.current_system]
            player=self.pl_data[user]
            time=self.get_game_time()
            response=llm.generateResponse(f'时间:{time}\n玩家{user}:{player}接取了任务,请你进行任务开场.',return_json=True)
        else :
            llm: LLMAPI = self._sub_model_dict[self.current_system]
            player = self.pl_data[user]
            time = self.get_game_time()
            response = llm.generateResponse(f"{time}\n{text}", return_json=True)
        # TODO: 用工具函数判断返回的信息.任务完成/正常对话. 任务完成-玩家信息修改,transfer
        if ():
            # 更新玩家资源待完善
            self.pl_data[user]['resource']=response.get('resource')
            response = llm.generateResponse(f'请你进行任务总结.', return_json=True)
            self.trans_control("Main")
            time=self.get_game_time()
            response = llm.generateResponse(f'时间:{time}\n玩家{user}:{player}完成了任务,以下是任务完成的梗概.{response["choices"][0]["message"]["content"]}', return_json=True)
            return response
        else:
            return response

    def accept(self,task_name):
        # TODO:根据任务状态,返回不能接任务\接取任务,更新任务状态,转交控制权(回到chat中).
        if self.quest_list[task_name]['status']:
            self.quest_list[task_name]['status']=0
            self.trans_control(task_name)
            return True
        return False

    def init(self,data):
        # TODO: 存玩家数据并初始化系统和任务(使用工具).返回主系统问候.
        '''

        :param data:
        玩家数据:
        - 名字
        - 描述信息
        - 初始资源:
            - 具体资源a
            - 具体资源b
            - 具体资源c
        :return:
        '''
        player=data.get('player_name')
        player_info=data.get("player_info")
        player_resource=data.get("resource")
        self.pl_data[player]={
            'player_info':player_info,
            'resource':player_resource
        }
        task_name,task_info,task_model=task_generate('互动任务')
        '''
        task_info:{
                "info":任务描述
                "status":任务状态
            }
        '''
        task_info['user']=player
        self.quest_list[task_name]=task_info
        self._sub_model_dict[task_name]=task_model
        # 创建主系统
        main_model = LLMAPI("KIMI-server", self.bg)
        self._sub_model_dict['Main'] = main_model
        response = self.chat({"text":f'以下是玩家信息:\n姓名:{player}\n描述:{player_info},请你进行游戏开场问候'})
        self.start_game()
        return response

    def get_quest(self,data):
        # 调用任务生成
        player=data.get('role')
        task_type=data.get('task')
        description=data.get('description','任意')
        quest_name,quest_info,quest_Model=task_generate(task_type,description)
        quest_info['user']=player
        self.quest_list[f'{quest_name}']=quest_info
        self._sub_model_dict['quest_name']=quest_Model
        return {'quest_name':quest_name,'quest_info':quest_info}

    @property
    def quest_list(self):
        return self._quest_list
    @quest_list.setter
    def quest_list(self, value):
        self._quest_list = value

    @property
    def sub_model_dict(self):
        return self._sub_model_dict
    @sub_model_dict.setter
    def sub_model_dict(self, value):
        self._sub_model_dict = value

    @property
    def pl_data(self):
        return self._pl_data
    @pl_data.setter
    def pl_data(self, value):
        self._pl_data = value

    def save(self, filename):
        '''
        保存当前状态到文件
        :param filename: 保存文件的名称
        :return: None
        '''
        self.pause_game()
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
        print(f"Game state saved to {filename}")

    @staticmethod
    def load(filename):
        '''
        从文件读取状态
        :param filename: 读取文件的名称
        :return: Backend实例
        '''
        with open(filename, 'rb') as file:
            backend_instance = pickle.load(file)
        print(f"Game state loaded from {filename}")
        return backend_instance
