'''
在这个文件中,我定义了一个KimiChat类,用于与大模型进行对话
沿用了read_answer文件用于提取信息
'''

import requests
from Authorization import Headers

class KimiChat:
    def __init__(self, model_name='kimi', use_search=False, stream=False):
        '''
        :param model_name: 当使用kimi+智能体，model请填写智能体ID，就是浏览器地址栏上尾部的一串英文+数字20个字符的ID
        :param use_search:是否开启联网搜索，默认false
        :param stream:如果使用SSE流请设置为true，默认false
        参数说明:
        base_url:服务器端口,这里采取的是本地搭箭的服务器(我使用的是node搭箭)
        headers:头部,具体内容在Authorization文件中(便于管理key)
        '''
        self.base_url = "http://127.0.0.1:8000/v1/chat/completions"
        self.model_name = model_name
        self.use_search = use_search
        self.stream = stream
        self.headers = Headers
    def create_request_body(self, user_message):
        '''
        :param user_message: 对话内容
        :return: 一个字典,包含请求数据
        '''
        return {
            "model": self.model_name,
            "conversation_id":"null",
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "use_search": self.use_search,
            "stream": self.stream
        }

    def send_message(self, user_message, id=None):
        '''

        :param user_message: 发送的信息
        :param id: 对话id,默认为None
        :return: 大模型返回的信息,以json的格式
        '''

        request_body = self.create_request_body(user_message)
        if id is not None:
            request_body["conversation_id"] = id

        try:
            response = requests.post(self.base_url, headers=self.headers, json=request_body)
            response.raise_for_status()  # 如果响应状态码不是200，将抛出异常
            return response.json()  # 返回JSON格式的响应数据
        except requests.exceptions.HTTPError as errh:
            return f"HTTP Error: {errh}"
        except requests.exceptions.ConnectionError as errc:
            return f"Error Connecting: {errc}"
        except requests.exceptions.Timeout as errt:
            return f"Timeout Error: {errt}"
        except requests.exceptions.RequestException as err:
            return f"Error: {err}"

def read_answer(answer):
    '''
    :param answer:待提取的返回数据
    :return:
    - id: 对话id
    - content: 对话内容
    '''
    if answer == -1:
        print("啊，kimi挂了~")

    id = answer["id"]
    content = answer["choices"][0]["message"]["content"]
    print(content)

    return id, content

