
### 代码规范

**对于每个文件夹，请创建一个空的 `__init__.py` 文件，以方便其他部分进行引用**。

为了保证代码的可读性和可维护性，写程序时请至少遵守以下内容。
- 引用项目时，分成三个部分：
    - python 内置的模块作为第一部分
    - python 没有内置的模块作为第二部分
    - 本地的模块作为第三部分。
如
```python
# 内置模块
import os
import sys
# 需要 pip 的模块
import openai
import pygame
# 本地
from request.Request import (get_request_kimi, read_answer, get_request_chatGPT)
```
- 对于部分复杂的函数(无法一眼看到其功能)，请使用注释进行解释。解释基于 `Docstring` 的格式。文档风格采用 `Google` 风格。

```python
def func(arg1:int, arg2:str, arg3:list = []):
    """
    _A short summary of this function_

    (Optional) _A detailed description of this function_
    
    Args:
        arg1 (int): _description_
        arg2 (int): _description_. Defaults to 0.
        arg3 (list): _description_. Defaults to [].
    
    Returns:
        _type_: _description_
    
    Raises:
        AssertionError: _description_
    
    """
    # the function body.
```

对于类的描述，采取 如下形式
```python
class TheClass(object):
    """
    _A short summary of this class_

    (Optional) _A detailed description of this class_
    
    Attributes:
    ---
        - _attribute1_ (type): _description_
        - _attribute2_ (type): _description_
        - _attribute3_ (type): _description_
    
    Methods:
    ---
        _method1_ (type): _description_
        _method2_ (type): _description_
        _method3_ (type): _description_
    """
```

特殊地，对于需要耦合的类，暴露的接口请额外写在程序最前面，或另创建一个文档进行描述。

为了可维护性，建议
- `constant.py` 用来储存所有的常变量，并请全大写以作区分。
- `prompt.py` 用来储存对应的 `prompt` 以供直接使用。

### `git commit` 规范
如果允许，对于有项目影响的 `commit` 可参考如下规范
```bash
<type>(<scope>): <subject>
```
`type` 说明 `commit` 的类别，可采用 
- `feat` 增加新功能。
- `fix` 修复 bug.
- `docs` 文档修改。
- `style` 代码格式修改，不影响代码逻辑。
- `refactor` 重构代码，理论上不影响现有功能。

`scope` 说明 `commit` 影响的范围，比如数据层、控制层、视图层等等。

`subject` 是 `commit` 的概述，可以简明地描述 commit 的作用。

如
```bash
git commit -m "(doc) rewrite the whole README.md file."
```