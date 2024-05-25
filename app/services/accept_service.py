def handle_accept_request(data):
    text = data.get('text', '')
    role = data.get('role', '')
    # TODO:处理接受任务逻辑
    status:bool = True  # 假设任务接受成功
    return {"status": status}
