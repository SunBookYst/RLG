def handle_feedback_request(data):
    text = data.get('text', '')
    role = data.get('role', '')
    # TODO:处理子任务交互逻辑
    return {"text": text, "role": role}
