import os
import json
import requests
from utils import show_ui, show_loading,show_options,thread_action,chat,create_bg
from colorama import Fore, Back, Style
import threading



if __name__ == "__main__":
    show_ui()
    # 请选择你的角色 #TODO
    print(Fore.RED+"·请选择你的角色")
    Style.RESET_ALL
    roles = ["刘备","孙权","曹操","随机"]
    role = roles[show_options(roles)]
    s = "正在生成你的剧情"
    # s0 = ""
    res = thread_action([create_bg,show_loading],[[s],[],[]])
    chat(res[0])