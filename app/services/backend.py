import time
import pickle
from datetime import datetime, timedelta
from RLG.utils import *
class backend(object):
    '''
    后台系统类
    '''
    def __init__(self,time_set=40,debug=False):
        '''
        :param bg:给主系统的prompt
        :param time_set: 时间流苏,每多少分钟过去一天
        :param debug: 是否打印信息 Default:False
        '''
        # 主要模型
        self.task_generator=None
        self.bg_generator=None
        self.sd=None
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
            print(f'fail to transfer control from {self.current_system} to {sys_name}\n{sys_name} not recognized')
            return
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
        if self.current_system=='Main':
            DM=self._sub_model_dict['Main']
            response=talk_to_dm(DM,data)
        else:
            j,director,last_play=self._sub_model_dict[self.current_system]
            end,response=task_play(director,j,data,last_play)
            response['status']=False
            self.sub_model_dict[self.current_system][2]=response
            if end==True or end=="True":
                self.current_system='Main'
                task=self.quest_list[self.current_system]
                self.pl_data['resource']+=task['reward']
                self._sub_model_dict.pop[self.current_system]
                self.quest_list.pop[self.current_system]
                response['status']=True
        return response

    def accept(self,task_name):
        task=self.quest_list[task_name]
        if task['status']:
            j,task_director,start_response=task_init(task)
            task['status'] = False
            self._sub_model_dict[task_name]=(j,task_director,'start')
            self.trans_control(task_name)
            return start_response
        return {'text':"该任务当前不可接受",'role':'Main'}

    def init(self,data):
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
        Main_sys, task_generator, bg_generator, sd=initialize_system()
        self._sub_model_dict['Main']=Main_sys
        self.task_generator=task_generator
        self.bg_generator=bg_generator
        self.sd=sd
        task=task_generate(task_generator,'初始任务')
        task['status']=True
        self.quest_list[task['task_name']]=task

        response=talk_to_dm(Main_sys,f'玩家信息:{player_info}\n请你进行游戏开场白')
        self.start_game()
        return response

    def generate_task(self,data):
        # 调用任务生成
        player=data.get('role')
        task_type=data.get('task')
        description=data.get('description','任意')
        task=task_generate(self.task_generator,task_type,description)
        task['status']=True
        self.quest_list[task['task_name']]=task

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
