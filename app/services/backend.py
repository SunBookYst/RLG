import time
import pickle
from datetime import datetime, timedelta
from RLG.Request.llmapi import LLMAPI

user_sessions={}

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
        # 创建主系统
        main_model=LLMAPI("KIMI-server",bg)
        self._sub_model_dict['Main']=main_model
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
        text = data.get('text', '')
        role = data.get('role', '玩家')

        if self.debug:
            print(f"generate response from {self.current_system},text:{text}")
        llm:LLMAPI = self._sub_model_dict.get(self.current_system)
        response= llm.generateResponse(text)
        return {'text': response, "role": self.current_system}


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
