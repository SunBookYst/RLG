
import requests

import openai

from RLG.Request.constant import (GPT_CLIENT, KIMI_CLIENT, TOKEN_HEADERS, SERVER_URL)
from RLG.Request.constant import MAX_WINDOW

class LLMAPI(object):
    """
    The common API used to interact with the LLM models.

    Attributes:
    -----------
        - model_name (str): The name of the LLM model to use, now support (GPT-3.5-turbo, kimi, KIMI-server)
        - initial_prompt (str): The initial prompt to start the conversation, default is an empty string
        - chat_history (list): The history of the conversation, make a consistent chat.
        - kimi_id (str): The ID of the kimi model, default is "null"
            (So to get rid of a 'init' function first.)
            
    Methods:
    --------
        - generateResponse(prompt, return_json = False): Generate a response from the LLM model.
    """
    
    def __init__(self, model_name, initial_prompt = ""):
        self.model_name = model_name
        self.initial_prompt = initial_prompt
        
        if initial_prompt == '':
            self.chat_history = []
        else:
            self.chat_history = [{'role': 'system', 'content': initial_prompt}]
        self.kimi_id = 'null'

    def generateResponse(self, prompt:str, return_json:bool = False):
        """
        Generate a result from a given prompt.


        Args:
            prompt (str): the input prompt
            return_json (bool, optional): a boolean variable, return the raw json if set True, or only return the text if set False. Defaults to False.

        Raises:
            Exception: Server Error. If the server is not properly set up, and the request fails.

        Returns:
            str|dict: if the return_json is set to False, return the text of the response. If the return_json is set to True, return the raw json of the response.
        """
        prompt = self.initial_prompt + prompt
        
        self.chat_history.append({'role':'user', 'content': prompt})
        
        if self.model_name == "gpt-3.5-turbo":

            response = GPT_CLIENT.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = self.chat_history[-MAX_WINDOW:],
            )
            
            self.chat_history.append({'role':'assistant','content': response.choices[0].message.content})
            
            if return_json:
                return response
            else:
                response = response.choices[0].message.content
                return response
        
        if self.model_name == "kimi":
            
            response = KIMI_CLIENT.chat.completions.create(
                model = "moonshot-v1-8k",
                messages=self.chat_history[-MAX_WINDOW:]
            )
            
            self.chat_history.append({'role':'assistant','content': response.choices[0].message.content})
            
            if return_json:
                return response
            else:
                response = response.choices[0].message.content
                return response
                
        if self.model_name == "KIMI-server":
            
            data = {
                "model": "kimi",
                "conversation_id": self.kimi_id,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "use_search": True,
                "stream": False
            }
                
            response = requests.post(url = SERVER_URL, headers = TOKEN_HEADERS, json = data)
            
            if response.status_code != 200:
                raise Exception("Server error")
            
            response = response.json()
            
            if self.kimi_id == 'null':
                self.kimi_id = response['id']
            
            if return_json:
                return response
            else:
                response = response["choices"][0]["message"]["content"]
                return response


def main():
    
    Q = "你是谁？"
    
    try:
        llm_server = LLMAPI("KIMI-server")
        response = llm_server.generateResponse(Q)
        print('kimi-server:',response)
    
    except Exception as e:
        print('kimi-server: 连接失败')
        print(e)
        
    try:
        llm_gpt = LLMAPI("gpt-3.5-turbo")
        response = llm_gpt.generateResponse(Q)
        print('gpt-3.5-turbo:',response)
        
    except Exception as e:
        print('gpt-3.5-turbo: 连接失败')
        print(e)
    
    try:
        llm_kimi = LLMAPI("kimi")
        response = llm_kimi.generateResponse(Q)
        print('kimi:',response)
        
    except Exception as e:
        print('kimi: 连接失败')
        print(e)
    
if __name__ == "__main__":
    main()