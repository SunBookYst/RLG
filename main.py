import os
import sys_groundstory.sys as sys
import time
def main():
    # TODO:生成地图
    t=time.strftime("%Y-%m-%d&%H:%M:%S",time.localtime())
    with open(f'./log{t}.txt','a',encoding='utf-8') as f:
        qid,outline=sys.init_quest()
        id,content=sys.init()
        f.write(content)
        id,content=sys.call_sys(id,outline+"\n现在，请你仔细阅读大纲，以【系统】xxx的格式进行背景故事简介。等待玩家的设定的输入。")
        f.write(content)
        id,content=sys.call_sys(id,"role:player 姓名:鲁道夫 超能力:拥有[肉体强化]魔法 身份：退伍军人。 请你阅读玩家的设定，以【系统】xxxxx的格式复述玩家的角色设定。")
        f.write(content)
        id,content=sys.call_sys(id,"请你阅读下面的示例，修正你的回答方式，并说明冒险引子"
                             "## 根据玩家输入，进行对话生成，示例："
                             "输入："
                             "请说明冒险引子"
                             "生成结果："
                             "【系统】深水城，光辉之城，北地之冠冕，剑湾北地的一颗璀璨明珠，一个商业发达，治安稳定，民众安居乐业的大都市。虽然深水城的历史历经数次大规模破坏，不过顽强的深水城依旧屹立百年而不倒。深水城并非什么异端异族所占据的排外都市，也并非什么军阀割据的武装要塞，这里也绝非那种目不识丁的农民聚集的农庄小镇。这里是矗立在由正义之神打造的律法之上的富饶城邦。"
                             "【系统】时至冬末，二月中，你收到你们的老友——瓦罗——的一封信。信件里，这位老友一如既往的牛皮不停，废话不息，但尽管如此，这位老友还是略显苦涩地邀请你来到深水城中的哈欠门酒馆，来面谈。明显，这位老友有求于人。"
                             "输入："
                             "【玩家】（我现在在哪里？）"
                             "生成结果："
                             "【系统】你在深水城的城门口，城门高耸而宏伟。你看到成群结队的守卫，在城门口来回巡逻，过往商贩依次有序进入，入城的手续有些繁琐，不过只要保持耐心，很快就能进入城中。"
                             "输入:"
                             "【玩家】（我知道那个酒馆怎么走吗）"
                             "生成结果:"
                             "【系统】你不是本地人，你第一次来到深水城，并不知道哈欠门酒馆怎么走。不过，你或许可以问问路人，比如门口的门卫。"
                             "输入："
                             "【玩家】“劳烦问一下！”#在卫兵面前努力踮起脚尖，举起双手引起注意“哈欠门酒馆怎么走啊？”一边问，一边把准备好好的证件拿出来举到他面前。"
                             "生成结果："
                             "【法官】“哈欠门啊。”#一边接着审视着你身后那个兽人的文件，一边说，“城堡区，最显眼那个就是。”"
                             "【系统】穿越北门，向着南方望去，面前的隐约可见的，正是骄傲的深水山，那巍峨的身影坐落在西南的天际线上，直抵大海。")
        f.write(content)
        # TODO:导入地图,进行任务调度,导入玩家设定
        while True:
            print('[e]退出游戏')
            talk=input('玩家:')
            if talk=='e':
                id,content=sys.summerize(id)
                with open('save.txt','w',encoding='utf-8') as logs:
                    logs.write(str(id))
                    logs.write('\n'+content)
                exit()
            pl_talk='【玩家】'+talk
            f.write('\n'+pl_talk+'\n')
            id,sys_content=sys.call_sys(id,pl_talk)

if __name__ == '__main__':
    main()