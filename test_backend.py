from app.services.backend import backend
from RLG.Request import llmapi
if __name__ == '__main__':
    test_backend=backend('你是一个游戏的主系统,现在我正在对游戏进行测试',debug=True)
    test_backend.start_game()
    print('\n---获取时间测试---')
    time=test_backend.get_game_time()
    print(time)
    print('\n---对话测试---')
    answer=test_backend.chat({"text":"你好","role":"testing Engineer"})
    print(answer)
    print('\n---任务列表,模型列表,角色信息增删查测试---')
    test_backend.quest_list['quest1']='this is Q1'
    test_backend.pl_data['player1']='this is player1'
    print("任务列表:{test_backend.quest_list}, 玩家信息:{test_backend.pl_data}")
    test_backend.sub_model_dict['1']=llmapi.LLMAPI('KIMI-server',"你是一个游戏的任务系统,现在我在对你进行测试.")
    print('\n---切换控制权测试---')
    test_backend.trans_control('1')
    answer=test_backend.chat({"text":"请你生成一个任务","role":"testing Engineer"})
    print(answer)
    print('\n---存取测试---')
    test_backend.save('./save/test_game.pkl')
    loaded_backend_system = backend.load('./save/test_game.pkl')
    loaded_backend_system.start_game()
    print(loaded_backend_system.get_game_time())
    loaded_backend_system.trans_control('Main')
    print(loaded_backend_system.chat({"text":"你是谁","role":"testing Engineer"}))
    print(loaded_backend_system.get_game_time())
    loaded_backend_system.save('./save/test_game.pkl')