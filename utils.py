import time
from colorama import Fore, Back, Style
import openai
import threading

event = threading.Event()
openai.api_key = "sk-j3JvDVdinEntkcLnB4F8Ba4cBf674015Bf8e860dBd26625c"
openai.base_url = "https://free.gpt.ge/v1/"
openai.default_headers = {
    "x-foo":"true"
}


class ThreadWithReturnValue(threading.Thread): # 使得线程结束附带一个返回值
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        super().join()
        return self._return

def thread_action(func_list,args_list):
    threads = []
    res = []
    for i in range(len(func_list)):
        threads.append(ThreadWithReturnValue(target=func_list[i],args = args_list[i]))
        threads[i].start()
    res =[]
    for i in range(len(func_list)-1):
        res.append(threads[i].join())
    event.set()
    res.append(threads[-1].join()) #最后一个函数默认为加载，读条到此结束
    event.clear()
    return res

def create_bg(s): #创建游戏故事背景，任务线等等
    print(Fore.YELLOW+s)
    message = get_first()
    print(Style.RESET_ALL,end='')
    return message

def show_loading(s="",s2="加载完毕"):
    while not event.is_set():
        for char in '|/-\\':
            print(Fore.YELLOW+f"\rLoading {char}"+s, end='')
            print(Style.RESET_ALL,end='')
            time.sleep(0.1)
    else:
        print('\r' + ' ' * 80 + '\r', end='')
        print(Fore.YELLOW+s2)
        print(Style.RESET_ALL,end='')

def show_options(options):
    print(Fore.BLUE,end='')
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")
    while True:
        index = input("您的选择为")
        if index not in [str(i+1) for i in range(len(options))]:
            print(Fore.RED+"请重新选择!")
            continue
        else:
            break
    print(Style.RESET_ALL,end='')
    return int(index)-1


def get_first():
    prompt = """请以游戏文案设计师的视角，帮助我完成一部三国主题的文字冒险对话游戏的情节设计和文案，我作为刘备参与这个游戏。

            **游戏玩法**：游戏会给出初始背景、初始事件、初始选项，玩家选择选项后，触发相应事件。事件又会给出多个新选项，玩家选择新选项进而触发新事件，最终达成不同的结局。选项可以表现为玩家与npc对话，也可以表现为玩家在事件中决策。

            **文案规则**：
            1. 整体文案形式：以表格呈现，包括两列：第一列是“触发语”，触发语代表玩家选择的选项，包括初始选项、选项触发事件对应的后续选项；第二列是“显示语”，显示语代表“触发语”对应的显示内容，包括场景、触发的事件、事件提供的新选项。注意，“显示语”中的事件可以提供两个选项，而“触发语”必须是“显示语”中的某个选项。
            2. 如何描述场景：50字左右，包含时间、地点、人物、意义。
            3. 如何描述事件：标好对应的选项，因为除了初始事件外，其他事件必须与一个选项相对应。标好序号（如：“事件2”），保证每一个事件的序号是唯一的。60字左右。
            4. 如何描述选项：标好序号串（如：“选项2-3”，这表示“事件2”中的第3个选项）。选项尽可能简洁，不超过10个字
            5. 如何描述结局：标好对应的选项，因为结局必须与某些选项相对应。
            **文案示例**：
            |触发语|显示语|
            |-|-|
            |开始游戏|场景：一个繁华的商业街区，人群熙攘，你独自一人走在街道上，忽然看到一个神秘的小巷，小巷的拐角处有一扇破旧的门，门上的牌子写着“神秘的魔法展览”。<br>事件1：你好奇地走近门口，感受到门后面传来一股神秘的气息。你看到一个穿着黑袍的男子站在柜台前，他向你示意靠近一些。你察觉到他手里拿着一张卡片，上面写着“免费入场券”，你开始想了解一下这个神秘的魔法展览。 <br>选项1-1：询问对方 <br>选项1-2：不想了解|
            |选项1-1：询问对方|事件2：男子微笑着，递给你一张小册子，上面写着“魔法展览导览”，然后开始向你讲解魔法的奥秘。你似乎被他的话语所吸引，开始对这个神秘的魔法世界充满好奇。<br>选项2-1：“我想深入了解魔法！”<br>选项2-2：表示质疑|
            |选项1-2：不想了解|事件3：男子微笑着说：“没关系，这里的确不是适合所有人的地方。”他递给你一张小卡片，上面写着“如果你改变主意，欢迎再来”，然后向你告别。 <br>选项3-1：遗憾离开 <br>选项3-2：参加展览|
            |选项3-2：参加展览|结局：“光明魔法”：你重新来到魔法展览，更深入地了解了魔法世界，学习到了许多神奇的魔法知识，对魔法的兴趣更加浓厚，你开始探索这个神秘的展览|

            学习以上材料的格式，生成三国主题游戏文案示例。"""
    messages = []
    messages.append({"role":"user","content":prompt})
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    # print(Fore.GREEN+"系统:",Style.RESET_ALL+completion.choices[0].message.content)
    return completion.choices[0].message.content


def chat(m):
    history = []
    # first_stage = True
    # TODO从历史对话中加载内容
    while True:
        messages = history[-10:]
        # if first_stage:
            # message = get_first() # XXX 诱导生成游戏初始文案，随着对话加长，这个信息可能会被抛弃，需要替代方案
            # first_stage = False
            # print("游戏设定加载成功")

        history.append({"role":"user","content":m}) #NOTE 装作用户输入的游戏设定
        history.append({"role":"assistant","content":"好的，我将记住这个游戏背景"})
        message = input("") #TODO 更为理想的设计应该是 在这里列出选项，选项可以由GPT给出，我们整理后列出
        if message.lower() == "stop":
            break
        if message.lower() == "save":
            pass #TODO 保存聊天上下文
        messages.append({"role":"user","content":message})
        history.append({"role":"user","content":message})
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        print(Fore.GREEN+"系统:", Fore.LIGHTBLACK_EX+completion.choices[0].message.content, Style.RESET_ALL)
        history.append({"role":"assistant", "content": completion.choices[0].message.content})
    return


def show_ui():
    print(Fore.RED+"""

                         ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░ 
                            ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
                            ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
                            ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░   
                            ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
                            ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
                            ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░ 

  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓██████████████▓▒░ ░▒▓███████▓▒░ 
  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
  ░▒▓███████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  
  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ 
  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ 
  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  
                                                                                                          """)
    print(Style.BRIGHT + "欢迎来到三国乱世！")
    print(Style.RESET_ALL)