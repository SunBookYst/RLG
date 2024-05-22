import RLG.Request.Request as req

def init_quest():
    with open('./sys_groundstory/quest_sys_prompt.txt','r',encoding='utf-8') as f:
        quest_prompt=f.read()
    q_re=req.get_request_kimi(None,quest_prompt)
    q_id,outline=req.read_answer(q_re,show=False)
    with open('./outline.txt','w',encoding='utf-8') as f:
        f.write(outline)

    return q_id,outline

def init(load_log:bool=False):
    '''
    :param load_log:默认False,读取log的时候请改为True(尚未实现load功能)
    :return: id,content,
    '''
    if load_log:
        print('此功能尚未实现')
        pass
    with open('./sys_groundstory/sys_prompt.txt','r',encoding='utf-8') as f:
        sys_prompt=f.read()
    response=req.get_request_kimi(None,sys_prompt)
    id,content=req.read_answer(response)

    return id,content
def call_sys(id,content):
    '''
    请注意初次对话请先调用init
    :param id:
    :param content:
    :return: id,content
    '''
    response=req.get_request_kimi(id,content)
    return req.read_answer(response)

def summerize(id):
    '''
    实验性内容：让大模型自行生成总结性内容以便保存进度
    :param id:
    :return:
    '''
    id,s=call_sys(id,'玩家选择在这里暂停游戏，请你根据目前为止游玩的内容，生成一份概括，进行存档。')
    return id,s
