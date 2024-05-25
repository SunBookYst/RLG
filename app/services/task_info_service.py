def handle_task_info_request(data):
    role = data.get('role', '')
    # TODO:获取任务清单逻辑
    task_list = ["task1", "task2", "task3"]
    return {"task_list": task_list}
