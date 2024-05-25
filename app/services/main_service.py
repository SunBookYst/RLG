from ...Request.llmapi import LLMAPI

user_sessions={}

def handle_main_request(data,user_id):
    '''
    和DM系统对话?
    :param data: {'text':str,'role':str}
    :return:{'text':str,'role':str},'role' default to '系统'
    '''
    text = data.get('text', '')
    role = data.get('role', '玩家')
    # TODO:处理主界面交互逻辑
    if user_id not in user_sessions:
        # 这里要一个DM系统的实例化,完成背景信息导入
        with open('../prompts/background.txt','r',encoding='utf-8') as f:
            bg=f.read()
        user_sessions[user_id] = LLMAPI('KIMI-server',bg)

    llm_api = user_sessions[user_id]
    response_text=llm_api.generateResponse(text)
    return {"text": response_text, "role": '系统'}
