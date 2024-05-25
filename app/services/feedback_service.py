#from ...subsenario import
'''
    导入子任务接口
'''
def handle_feedback_request(data):
    text = data.get('text', '')
    role = data.get('role', '')
    # TODO:处理子任务交互逻辑
    # 对话子系统
    return {"text": text, "role": role}
