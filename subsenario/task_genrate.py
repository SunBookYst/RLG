from request.llmapi import initialize_llm


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


def task_generate(task_type, description="任意的"):
    # 需求定制
    need = f"帮我生成一个{description}的{task_type}"

    # 初始化模型
    task_prompt = read_file("task")
    task_generator = initialize_llm(task_prompt)
    act_prompt = read_file("task_acting")
    task_director = initialize_llm(act_prompt)

    task = task_generator.generateResponse(need)
    print(task)

    play = task_director.generateResponse(task)
    print(play)


if __name__ == "__main__":
    task_generate("互动任务")
