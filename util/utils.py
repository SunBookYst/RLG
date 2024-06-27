DEBUG = True

def debug_print(*args):
    """
    A function to print debug information.

    Args:
        *args: the arguments to be printed.
    """
    if DEBUG:
        for a in args:
            if type(a) == dict:
                for k,v in a.items():
                    print(f'{k}:{v}')
            else:
                print(a)

def fix_response(origin_text: str, attr: str):
    """
    Extract json information by retreiving text from {}
    Fix the response by removing all the \n to '\n'. A better way to fix this is to change the prompt.

    Args:
        origin_text (str): the origin text generated by the LLMs.
        attr (str): the attribution whose value need to be fixed.

    Returns:
        str: the fixed text.
    """
    lindex = origin_text.find('{')
    rindex = origin_text.find('}')
    if lindex != -1 and rindex != -1:
        origin_text = origin_text[lindex: rindex+1]
    
    index = origin_text.find(attr)
    if index == -1:
        return origin_text
    
    else:
        lquote = origin_text.find('"', index + len(attr) + 1)
        rquote = origin_text.find('"', lquote + 1)
        content = origin_text[lquote: rquote + 1]
        content = "\\n".join(content.split("\n"))
        text = origin_text[:lquote] + content + origin_text[rquote + 1:]

        return text
    