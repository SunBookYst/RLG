import requests
import openai

from request.Authorization import headers
url="http://127.0.0.1:8000/v1/chat/completions"

def get_request_kimi(id, content):
    '''
    request for kimi
    :param id:
    :param content:
    :return:
    '''
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


def read_answer(answer,show=True):
    '''
    :param answer:
    :param show:True -当不希望打印内容时,设置为Fals
    :return:
    '''
    if answer == -1:
        print("Error: No answer")
        return 0,'Null'

    id = answer["id"]
    content = answer["choices"][0]["message"]["content"]
    if show:
        print(content)
    return id, content

def get_request_chatGPT(id,content):
    '''

    :param id:对话id
    :param content:对话内容
    :return: json格式的对话
    '''
    # TODO
    pass
    # return response.json()

