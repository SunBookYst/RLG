from request.llmapi import initialize_llm
from request.stable_diffusion_request import StableDiffusion
import json


def read_file(prompt_name):
    """
    读取文件内容。
    Args:
        prompt_name (str): prompt文件的名称。

    Returns:
        str: 文件内容。
    """
    with open(f"../prompts/{prompt_name}.txt", 'r', encoding='utf-8') as file:
        prompt = file.read()
    return prompt


def initialize_system():
    """
    当玩家登入时直接调用
    :return: DM、任务生成系统(task_generator)、背景生成系统(bg_generator)、绘图系统(sd)
    """
    # 初始化模型
    dm_prompt = read_file("DM")
    DM = initialize_llm(dm_prompt)
    task_prompt = read_file("task")
    task_generator = initialize_llm(task_prompt)
    bg_prompt = read_file('txt2img_background')
    bg_generator = initialize_llm(bg_prompt)
    sd = StableDiffusion()

    return DM, task_generator, bg_generator, sd


def task_generate(task_generator, task_type, description="任意"):
    """
    根据描述生成一个任务
    :param task_generator: 任务生成系统
    :param task_director: 任务演绎系统
    :param bg_generator: 背景生成系统
    :param sd: 绘图系统
    :param task_type: 任务类型
    :param description: 玩家期望的任务描述
    :return:dict{"task_name":（任务名称）,"task_description":（任务描述）,"attention":（注意事项）,"reward":（任务报酬）}
    """
    # 需求定制
    need = f"帮我生成一个{description}的{task_type}"
    task = task_generator.generateResponse(need, stream=True)

    return json.loads(task)


def talk_to_dm(dm, player_input=None):
    """
    用于跟dm对话
    :param dm: 玩家对应的dm
    :param player_input: 玩家的输入
    :return: 系统的回复，dict{"status":（玩家状态）, "role":"系统", "text":（系统回复）}
    """
    return json.loads(dm.generateResponse(f'【玩家】{player_input}'))


def task_init(play=None):
    """
    初始化一个任务，在玩家决定游玩时使用
    :param play: 任务综述
    :return: 裁判(j), 任务演绎系统(task_director), 演绎系统的第一句话
    """
    judge_prompt = read_file("judge")
    j = initialize_llm(judge_prompt, True)
    act_prompt = read_file("task_acting")
    task_director = initialize_llm(act_prompt)
    start = task_director.generateResponse(play)

    return j, task_director, start


def task_play(task_director, j, player_input=None, player_status=None, last_play=None):
    """
    与任务系统进行一轮对话
    :param task_director:任务演绎系统
    :param j:裁判
    :param player_input:玩家的输入
    :param player_status:玩家的状态
    :param last_play:上次的play，便于judge系统判断。第一次时为start
    :return: 任务系统的反馈(play), 游戏进程判断
    """
    content = f'{"system":{last_play}, "player":{player_input}, "player_status":{player_status}}'
    judge = json.loads(j.generateResponse(content))
    play = json.loads(task_director.generateResponse(f'【玩家】{player_input}'))
    return judge, play


if __name__ == "__main__":
    # 初始化模型
    '''
    dm_prompt = read_file("DM")
    DM = initialize_llm(dm_prompt)
    print(json.loads((DM.generateResponse("你好"))))
    task_prompt = read_file("task")
    task_generator = initialize_llm(task_prompt)
    print(json.loads((task_generator.generateResponse("给我一个任务"))))

    content = """
    {
        "text":"你站在苍穹大陆的东部边境，眼前是一片被迷雾笼罩的山谷——【龙息谷】。传说中，这里是龙族的栖息地，如今却显得异常寂静。你能感受到空气中弥漫着一股神秘而古老的力量。
        你的目标是寻找并带回失落的【龙眼】。你深吸一口气，踏入了这片未知的土地。山谷的入口处，有一块石碑，上面刻着一些模糊的符文，似乎隐藏着某种信息。
        请描述你接下来的行动。",
        "status": "1",
        "role": "None"
    }
    """
    bg_prompt = read_file('txt2img_background')
    bg_generator = initialize_llm(bg_prompt)
    sd = StableDiffusion()
    prompt = bg_generator.generateResponse(content)
    image = sd.generate_background(prompt)
    sd.process_images(image)
    '''
