
import requests
import json
from Request import KimiChat,read_answer

# 使用KimiChat类
kimi_chat = KimiChat(model_name="kimi",use_search=True)
#log=''
with open('DM_settings.txt','r',encoding='utf-8') as f:
    DM_settings=f.read()
with open('log.txt','w',encoding='utf-8') as file:
    # 发送消息给Kimi
    id, content = read_answer(kimi_chat.send_message(DM_settings))
    file.write(content+'\n')
    while True:
        #log=log+content+'\n'
        print('[q]退出游戏')
        player_content=input()
        if player_content=='q':
            break
        else:
            player_content='【玩家】'+player_content
            file.write(player_content+'\n')
            #log=log+player_content+'\n'
        id, content=read_answer(kimi_chat.send_message(player_content,id))
        file.write(content+'\n')

