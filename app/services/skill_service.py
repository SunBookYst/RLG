def handle_skill_request(data):
    role = data.get('role', '')
    # TODO:获取技能信息逻辑
    skills = {
        "skill1": "description1"
    }
    return {"skills": skills}
