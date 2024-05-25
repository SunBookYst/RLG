def handle_main_request(data):
    '''
    这是和什么系统对话的部分?
    :param data: {'text':str,'role':str}
    :return:{'text':str,'role':str},'role' default to '系统'
    '''
    text = data.get('text', '')
    role = data.get('role', '玩家')
    # TODO:处理主界面交互逻辑

    return {"text": text, "role": role}
