def handle_status_request(data):
    role = data.get('role', '')
    # TODO:获取人物信息逻辑
    attribute = {"物质": 100, "能量": 50, "经验": 10, "等级": 2}
    return {"attribute": attribute}
