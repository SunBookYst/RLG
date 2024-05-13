import requests

url = 'http://127.0.0.1:8000/v1/chat/completions'
token = ('eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyMzEzNDc5NiwiaWF0IjoxNzE1MzU4Nzk2LC'
         'JqdGkiOiJjb3Y0b2oydms2Z2ZpNHJobjlnMCIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjbWZvNHJlY3A3ZmZuYzR2dXQwMCIsInNwYWNlX2lk'
         'IjoiY21mbzRyZWNwN2ZmbmM0dnVzdmciLCJhYnN0cmFjdF91c2VyX2lkIjoiY21mbzRyZWNwN2ZmbmM0dnV0MDAifQ.rZQvnlZtPzYMXwlL1-a'
         'eTZ9oED81ciASCwksdN5ui80Ryb7zqvRn6ffos5Nx8QCce19OND02zXJz37-6AWNfag')


# 准备 headers
headers = {
    'Authorization': f"Bearer {token}"
}


def get_request(id, content):
    # 准备请求的数据
    data = {
        # model随意填写，如果不希望输出检索过程模型名称请包含silent_search
        # 如果使用kimi + 智能体，model请填写智能体ID，就是浏览器地址栏上尾部的一串英文 + 数字20个字符的ID
        "model": "kimi",
        # 目前多轮对话基于消息合并实现，某些场景可能导致能力下降且受单轮最大Token数限制
        # 如果您想获得原生的多轮对话体验，可以传入首轮消息获得的id，来接续上下文，注意如果使用这个，首轮必须传字符串'null'，否则第二轮会空响应！
        "conversation_id": 'null',
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        # 是否开启联网搜索，默认false
        "use_search": True,
        # 如果使用SSE流请设置为true，默认false
        "stream": False
    }

    if id is not None:
        data["conversation_id"] = id

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        return response.json()
    else:
        return -1


def read_answer(answer):
    if answer == -1:
        print("啊，kimi挂了~")

    id = answer["id"]
    content = answer["choices"][0]["message"]["content"]
    print(content)

    return id, content


def talk(id, content):
    id, content = read_answer(get_request(id, content))
    return id, content


def implant(id, content):
    return read_answer(get_request(id, content))


def pre_prompt(prompts):
    id = None
    content = None
    for prompt in prompts:
        id, content = implant(id, prompt)
    return id, content


