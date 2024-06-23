import os

PROMPT_PATH = os.path.join(os.path.dirname(__file__))

def get_prompt(relative_path: str) -> str:
    """
    Get a prompt from a file.

    Args:
        relative_path (str): the relative path of the prompt file

    Returns:
        str: the content of the prompt file
    """

    with open(os.path.join(PROMPT_PATH, relative_path), 'r', encoding='utf-8') as f:
        return f.read()
    

TASK_PROMPT = get_prompt('./prompts/task.txt')
EQUIPMENT_PROMPT = get_prompt('./prompts/equipment_craft.txt')
SKILL_PROMPT = get_prompt('./prompts/skill_generate.txt')
CUSTOM_PROMPT = get_prompt('./prompts/task_custom.txt')
BATTLE_PROMPT = get_prompt('./prompts/battle.txt')


DM_PROMPT = get_prompt("./prompts/DM.txt")
JUDGE_PROMPT = get_prompt("./prompts/judge.txt")
ACT_PROMPT = get_prompt("./prompts/task_acting.txt")

GENERATE_CHACTER_PROMPT = get_prompt("./prompts/txt2img_character.txt")
GENERATE_BACKGROUND_PROMPT = get_prompt("./prompts/txt2img_background.txt")