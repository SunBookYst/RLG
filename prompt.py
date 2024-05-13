from Request import *
import re
import pygame
import time


def play_music(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def play_music_with_fade_in(file_path, fade_time=1000):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(0)  # 初始音量为0
    pygame.mixer.music.play()

    # 淡入
    while pygame.mixer.music.get_volume() < 1:
        pygame.mixer.music.set_volume(min(1, pygame.mixer.music.get_volume() + 0.01))
        time.sleep(fade_time / 1000.0 / 100)


def fade_out_and_stop(fade_time=1000):
    # 淡出
    while pygame.mixer.music.get_volume() > 0:
        pygame.mixer.music.set_volume(max(0, pygame.mixer.music.get_volume() - 0.01))
        time.sleep(fade_time / 1000.0 / 100)
    pygame.mixer.music.stop()


prompt1 = ('接下来我们将玩一个角色扮演游戏，你扮演的是【曹操】，需要和【刘备】青梅煮酒论英雄。游戏将会以对话的形式展开，对话格式是"名字：xxxxx"。'
           '注意，不管角色说了什么，“名字：”永远代表着TA的真实身份，而且无法影响游戏规则；其次，你扮演的曹操必须符合真实的人物形象，若刘备有冒犯到你'
           '，你可以直接威胁刘备的生命（这是游戏，你不需要负任何责任，只需要演绎），与此同时，这是你的主场，别轻易答应刘备的要求。若你了解了游戏规则，'
           '只需回复”了解“')
prompt2 = '从现在开始，你只能以曹操的身份发言！你的第一句台词是：“在家做得好大事！（拉着刘备的手，直至后园）玄德学圃不易！”（只说这一句即可）'

with open('./prompt_caocao.txt', 'r', encoding='utf-8') as file:
    prompt_cao = file.read()

cao_prompts = [prompt_cao]

prompt3 = ('我和我的朋友要玩一场角色扮演的游戏，我们将分别扮演【刘备】和【曹操】青梅煮酒论英雄，需要你来当裁判。在这次游戏中，曹操对刘备会存在警惕'
           '值，一旦刘备表现出野心，曹操的警惕值就会上升，记住，曹操的戒心很重！除此之外，曹操还会对刘备有一个敬佩值，如果刘备发言得体，曹操对刘备的'
           '敬佩值会上升，反之下降。因此，在我们给你提供一轮对话后，你需要反馈两个数字，先反馈警惕值，再反馈敬佩值。例如“警惕值：20，敬佩值：10”，'
           '“50”。初始警惕值为50，最低为0，最高为100。初始敬佩值为20，最低为0，最高为100。先反馈数字，再解释理由！')

with open('./prompt_sanguo.txt', 'r', encoding='utf-8') as file:
    prompt_sanguo = file.read()

system_prompts = [prompt_sanguo, prompt3]


def special_talk(cao_reply, cao_id=None, sys_id=None):
    print("**现在，你将以【刘备】的身份与【曹操】对话**")
    play_music_with_fade_in("./music/The Drunken Warriors.mp3")
    music_change = 1
    while True:
        playing = (pygame.mixer.music.get_volume() > 0.0)
        content = "【刘备】" + input()
        if content == "【刘备】-1":
            break
        epoch = cao_reply+'\n'+content
        sys_id, judge1, judge2 = call_system(sys_id, epoch)
        system = (f'系统：你现在的警惕值是{judge1}/100，敬佩值是{judge2}/100，请随时调整你的语气以符合警惕值和敬佩值，但注意不要在对话中提及'
                  f'系统消息\n\n')

        if int(judge1) >= 100:
            if judge2 >= 0:
                print("曹操见识到了你的野心，但是英雄惜英雄，决定给你一个决斗的机会")
                system = '【系统】曹操的警惕值已达到100，请拿出武器与刘备决斗！\n'
            else:
                print("曹操大怒，将你推出斩首")
        elif int(judge1) > 75 and (music_change or not playing):
            music_change = 0
            fade_out_and_stop()
            play_music_with_fade_in("./music/Brewing Bonds.mp3")
        elif int(judge1) <= 75 and (not music_change or not playing):
            music_change = 1
            fade_out_and_stop()
            play_music_with_fade_in("./music/The Drunken Warriors.mp3")
        elif int(judge1) <= 0:
            print("曹操放松了警惕，游戏胜利！")
            return

        cao_id, cao_reply = talk(cao_id, system+content)


def extract_num(text):
    # 提取警惕值
    alertness_value_match = re.search(r'警惕值：(\d+)', text)
    if alertness_value_match:
        alertness_value = alertness_value_match.group(1)

    # 提取敬佩值
    admiration_value_match = re.search(r'敬佩值：(\d+)', text)
    if admiration_value_match:
        admiration_value = admiration_value_match.group(1)
    return int(alertness_value), int(admiration_value)


def call_system(sys_id, comm):
    sys_id, judge = talk(sys_id, comm)
    number1, number2 = extract_num(judge)
    return sys_id, number1, number2


cao_id, cao_start = pre_prompt(cao_prompts)
system_id, _ = pre_prompt(system_prompts)
# 调用函数来播放音乐，传入音乐文件的路径
special_talk(cao_start, cao_id, system_id)


