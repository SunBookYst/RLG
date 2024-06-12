Request List

- 主界面交互，发送:{'text':str,'role':str}; 路由：/main ; 期望接收：{'text':str,'role':str，'status':bool, subimg:base64 :Null},'role'默认为系统, status判断是否切换入任务系统，若非判断成功接收到任务，则一直返回False
- 子任务交互信息，发送：{'text': str, 'role': str}，即我的输入；路由：/feedback；期望接收：{'text':str,'role':str，'status':bool, npc_status: bool, image: base64/None} ，即与我交互的角色的反馈,status判断任务是否结束，若结束返回True
- 两个交互界面都需要判断是否是新的npc，若npc_status为True，则额外返回新的人物图片npc_status: bool, image: base64/None

### 下面的可以按需求随意整合
- 任务清单，发送：{'role': str }， 发送某个角色，给除这个角色可接受的任务清单；路由：/task_info；期望接收：{'task_list':[str,str,...]}，任务清单
- 人物信息，发送：{'role':str}; 路由：/status；期望接收: {'attribute':dict} #dict的key后端决定,可以包括物质，能量，经验，等级以及其他属性信息
- 背包信息，发送：{'role':str}; 路由：/bag；期望接收：{'equipments':dict} # key为物品名称，value需要统一一下，可以为list或者物品描述
- 技能信息，发送：{'role':str};路由：/skill； 期望接收：{'skills':dict} # key为技能名称，value需要统一一下，可以为list或者技能描述
- 合成界面，发送：{'role':str,'mode':0/1,'num':int,'des':str};路由：/merge； 期望接收：{'text':str} # 返回的文本可以描述一下新获得的物品, mode 0是合成技能,1是合成装备,des是对合成技能/装备的描述
<!-- -  -->
<!-- - 接受某任务，发送：{'text':str, 'role':str}；路由：/accept；期望接收：{'status':bool,''} -->
### 暂时不要紧的
- 当前时间，发送：{'role':str}；路由：/time；期望接收：{'time':str} 返回该角色对应的时间

- 检测合法性，发送：{'mode':0或1，'content':str}， 模式0检测姓名，模式1检测人物设定；路由：/legal；期望接收 {'status':bool}
<!-- - 可以改为init接口 -->
- 检测合法性，发送：{'mode':0 或 1，'content':str}， 模式0检测姓名，模式1检测人物设定；路由：/legal；期望接收 {'status':bool}

- 其他特殊事件（暂定），发送{'info':str,'role':str,'text':str}，描述任务，并附上玩家输入的text；路由：/others；期望接收：{’role':str,'text':str,'other':str}
- 其它系统，待定


- 登录 发送{'email':str,'password':str},前者为注册用的邮箱地址，后者为加密后的密码 ； 期望接收{'status_code':int,'username':str},username为注册时的用户名，status_code 200表示成功，其他还有如密码不正确，未注册等错误； 路由 /login
- 注册 发送{'email':str,'username':str,'password':str},email和password同上，需要注意username需要检测合法性； 期望接收 {'status_code':int},200为注册成功，其他code自定义，例如重名，邮箱已被使用，名称不合法等等；密码加密操作在前端完成； 路由/signup