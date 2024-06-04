from request.llmapi import initialize_llm, LLMAPI
from request.stable_diffusion_request import StableDiffusion
import json


def read_file(prompt_name):
    """
    read the file name.
    Args:
        prompt_name (str): the file name of the prompt stored.

    Returns:
        str: the content of the file.
    """
    with open(f"../prompts/{prompt_name}.txt", 'r', encoding='utf-8') as file:
        prompt = file.read()
    return prompt


def initialize_system():
    """
    The function to be called when the user is logged in.

    Returns:
        LLMAPI, LLMAPI, LLMAPI, StableDiffusion: The DM, task generator, background generator, and drawing system respectively.
    """

    # 初始化模型
    dm_prompt = read_file("DM")
    task_prompt = read_file("task")
    bg_prompt = read_file('txt2img_background')

    DM            :LLMAPI          = initialize_llm(dm_prompt)
    task_generator:LLMAPI          = initialize_llm(task_prompt)
    bg_generator  :LLMAPI          = initialize_llm(bg_prompt)
    sd            :StableDiffusion = StableDiffusion()

    return DM, task_generator, bg_generator, sd


def task_generate(task_generator, task_type, description="任意"):
    """
    Generate a task based on the task type and description.

    Args:
        task_generator (LLMAPI): The task generator.
        task_type (str): the type of the task
        description (str, optional): The detailed description of the task. Defaults to "任意".

    Returns:
        dict{}: The information of generated task.
    """

    # 需求定制
    need = f"帮我生成一个{description}的{task_type}"
    task = task_generator.generateResponse(need, stream=True)

    return json.loads(task)


def talk_to_dm(dm, player_input = None):
    """
    Talk to the DM according to the player's input and to the player's ID.

    Args:
        dm (LLMAPI): The DM model.
        player_input (str, optional): the player's input. Defaults to None.

    Returns:
        dict{}: The response from the DM.
    """
    return json.loads(dm.generateResponse(f'【玩家】{player_input}'))


def task_init(play=None):
    """
    Initialize the task when user selected.


    Args:
        play (str, optional): The overview of the task. Defaults to None.

    Returns:
        LLMAPI, LLMAPI, str: The judge system, the task director system, and the start statement of the task.
    """
    judge_prompt = read_file("judge")
    act_prompt = read_file("task_acting")


    j            :LLMAPI = initialize_llm(judge_prompt, True)
    task_director:LLMAPI = initialize_llm(act_prompt)
    start        :str    = task_director.generateResponse(play)

    return j, task_director, start


def task_play(task_director, j, player_input=None, player_status=None, last_play=None):
    """
    Make a round of conversation with the task director.

    Args:
        task_director (LLMAPI): the task generator of the task.
        j (LLMAPI): the judge of the task.
        player_input (str, optional): the user's input. Defaults to None.
        player_status (dict, optional): the user's current states. Defaults to None.
        last_play (dict, optional): the last round of the task. Defaults to None.

    Returns:
        dict{} dict{}: The feedback of the task director, and to judge the task process.
    """

    play_infos = {}
    play_infos["system"] = last_play
    play_infos["player"] = player_input
    play_infos["player_status"] = player_status

    content = json.dumps(play_infos)
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
