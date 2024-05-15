# OH YEAH
## Request
当前的架构采取kimi提供的GPT接口,在Request文件中.
## prompt.py
prompt.py中为一个简单的示例.采取的故事设定为:玩家扮演[刘备],GPT扮演[曹操],玩家的目标是通过对话让曹操的[警惕值]降低到阈值.
## prompt_caocao/prompt_sanguo.txt
存有曹操的人设和三国游戏的背景设定,给到GPT阅读.

## launch.py
也许可以从这里作为启动接口，提供了多线程函数的接口，可以实现如在加载时显示Loading等功能
启动效果演示
![example](https://github.com/Jaylen-Lee/image-demo/blob/main/RLG.png?raw=true)
stop结束游戏
save保存存档，但还未实现
## utils.py
一些功能性函数，以及gpt的接口，和上面kimi冲突