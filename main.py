import sys_groundstory.sys as sys

def main():
    # TODO:生成地图
    id,content=sys.init()
    # TODO:导入地图,进行任务调度,导入玩家设定
    while True:
        print('[e]退出游戏')
        talk=input('玩家:')
        if talk=='e':
            s=[sys.summerize(id)]
            with open('log.txt','r',encoding='utf-8') as logs:
                logs.write(s)
            exit()
        pl_talk='玩家'+talk
        id,sys_content=sys.call_sys(id,pl_talk)

if __name__ == '__main__':
    main()