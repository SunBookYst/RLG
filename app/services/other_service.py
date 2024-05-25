def handle_others_request(data):
    info = data.get('info', '')
    role = data.get('role', '')
    text = data.get('text', '')
    # TODO:处理特殊事件逻辑
    other_response = "This is a response to the special event."
    return {"role": role, "text": text, "other": other_response}
