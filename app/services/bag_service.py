def handle_bag_request(data):
    role = data.get('role', '')
    # TODO:获取背包信息逻辑
    equipments = {
        "item1": "description1"
    }
    return {"equipments": equipments}