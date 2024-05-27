# RLG_World

## 问题

- 游戏命名仍需界定。

    初版可以命名为 Heroes vs Villians。
- 系统会偶尔代替玩家做出行动（或者说，话太多）
- 系统会在末尾给出建议和选项询问玩家选择。

    上述内容通过完善 `prompt` 完成。

- 地图生成，任务生成，玩家属性，【制造系统】等子系统未接入。
    1. 地图生成是随机的，背景故事应当给出一些必要的建筑(市政厅、警察局、居民区、工厂等)，在地图生成时需要加入。
    2. 玩家属性仍未完成，需要设计一个类以供接入。

## 程序框架
```Apache
├─asset
├─app
   ├─services
├─request
├─src
├─sys_groundstory
├─ui
│  ├─asset
│  ├─image
│  ├─sound
```
其中
- `asset` 文件夹目前存储部分 Unity UI 文件以供后续使用。
- `app` 文件夹保存 `backend`类。
- `request` 文件夹保存 `Authorization`  (储存key并构建header) 和 `Request` (构建请求函数)文件。
- `sys_groundstory` 文件夹保存 `sys`和 `sys_prompt` 文件。构建系统。

- `src` 文件保存书写 `README.md` 相关的一些图片等。
- `ui` 文件夹是对 `RLG` UI 的设计部分，包含了一些基本的背景、图像和音频等。

## 更新 log
常规的 `commit` 和 `push` 通过 `comment` 来表示，无需写入此处。对于重大的项目更新，在此 `log` 下进行说明。 

### 5/21
- 加入了尝试性的summerize函数（在sys文件中），让大模型进行概括存档，还没有测试是否能读取存档。
- main文件，简单编写了问答以便进行测试。
- 更新了一些系统设置。

### 5/22 YSZ
- 重新修改了 `README.md` 文件。
### 5/27 CZY
- 完成了`backend`类的简单实现
  - 提供存取(需求pickle库)
  - 进行对话
  - 获取时间
  - 切换系统控制权(子系统接口)
  - 尚未对类进行规范的系统性注释
## 运行
**TODO**： 请在这里补全 KIMI API 使用的最小依赖。

reference: https://github.com/LLM-Red-Team/kimi-free-api/tree/master

运行 `main.py` 即可。

启动
```bash
pm2 start dist/index.js --name "kimi-free-api"
pause
```

停止
```bash
pm2 stop kimi-free-api
```

## 附

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





