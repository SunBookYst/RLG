import sys
sys.path.append('..')


from request.llmapi import LLMAPI

from prompt import GENERATE_CHOICE_PROMPT_1,GENERATE_CHOICE_PROMPT_2


class ChoiceSenario(object):
    
    def __init__(self):
        self.client = LLMAPI('gpt-3.5-turbo')
        
        
    def generateSenario(self):
        
        prompt = GENERATE_CHOICE_PROMPT_1.format(background = '一座平凡的城市', role = "无恶不作的恶徒") + GENERATE_CHOICE_PROMPT_2
        response = self.client.generateResponse(prompt)
        
        return response
    
    def run(self):
        
        event = self.generateSenario()
        
        try:
            event = eval(event)
        except:
            try:
                lbrace = event.find('{')
                rbrace = event.rfind('}')
                
                event = eval(event[lbrace:rbrace+1])
            except:
                print(event)
                # 生成失败。
                return
        
        print(event["description"])
        
        print(event["Choices"]["case1"]["description"])
        
        print(event["Choices"]["case2"]["description"])
        
        user_input = input('你要如何选择？[1/2]')
        
        if user_input == '1':
            print(event["Choices"]["case1"]["consequence_desc"])
        elif user_input == '2':
            print(event["Choices"]["case2"]["consequence_desc"])
        else:
            print('你跑了')
            
        
    
def main():
    
    sub = ChoiceSenario()
    
    sub.run()
    
    
if __name__ == '__main__':
    main()


