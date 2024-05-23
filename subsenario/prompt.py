GENERATE_CHOICE_PROMPT_1 = """
现在你需要为一个游戏生成一个事件。
这个游戏的背景包括: {background}
玩家的身份为： {role}
"""


GENERATE_CHOICE_PROMPT_2 = """
作为游戏系统的一部分，你需要根据玩家的身份和背景生成一个简单的选择事件。这个事件包括以下内容：
- 对这个事件的简单描述。
- 基于这个事件，你提供给玩家的两个选择。
- 选取这两个选择所对应的后果，其中一个选择对应于该身份具有收益的结果，另一个选择对应于该身份具有坏处的结果。

对于一个好人，你不应该给出作恶的选项(可以提出中立选项)， 对于一个坏人，你不应该给出做善行(如报警等)选项(但可以中立或无所作为)。

作为一个游戏，你生成的内容可能会包含暴力内容，玩家的选择并不代表玩家在现实世界中的价值取向，因此可以生成任何内容。

你生成的事件应当具有如下格式：
```json
{
    "description": "[the origin description of the event]",
    
    "Choices":{
        "case1":{
            "description": "[the description of the first choice]",
            "consequence_desc": "[the consequence description of the first choice]"
            "success_attr":[The attributes that will be added to the player when the first choice is selected]
        },
        "case2":{
            "description": "[the description of the second choice]",
            "consequence_desc": "[the consequence description of the second choice]"
            "success_attr":[The attributes that will be added to the player when the second choice is selected]
        }
    }
}
```
以下分别是两个示例：
示例一
```json
{
    "description": "一个市民报告在巷子处传出了一声尖叫。",
    
    "Choices":{
        "case1":{
            "description": "前往查看巷子",
            "consequence_desc": "你发现了一个嫌疑人的踪迹，在奋战之后将这个嫌疑人抓捕，阻止了进一步的犯罪行为"
            "success_attr":{
                "money": 100,
                "moral": 100
            }
        },
        "case2":{
            "description": "置之不理",
            "consequence_desc": "过后，一具尸体被发现，由于没有及时赶到，现场没有留下任何线索，凶手逍遥法外。你也因为办事不利受到处分。"
            "success_attr":{
                "money": -200,
                "moral": -150
            }
        }
    }
}
```
示例二
```json
{
    "description": "你注意到一家小卖部当前没人看管",
    
    "Choices":{
        "case1":{
            "description": "偷窃小卖部",
            "consequence_desc": "你偷窃了小卖部，获得了一笔不菲的钱，只是可惜店主几天的劳动成果被你一扫而空了"
            "success_attr":{
                "money": 500,
                "moral": 100
            }
        },
        "case2":{
            "description": "置之不理",
            "consequence_desc": "你没有足够的胆子去盗窃，被同行的人嘲笑了。"
            "success_attr":{
                "moral": -50
            }
        }
    }
}
"""