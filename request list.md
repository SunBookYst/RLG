Request List

- 主界面交互，发送:{'text':str,'role':str}; 路由：/main ; 期望接收：{'text':str,'role':str},'role'默认为系统

- 子任务交互信息，发送：{'text': str, 'role': str}，即我（某个角色）说的某句话，某个反应；路由：/feedback；期望接收：{'text':str,'role':str} ，即与我交互的角色的反馈
- 任务清单，发送：{'role': str }， 发送某个角色，给除这个角色可接受的任务清单；路由：/task_info；期望接收：{'task_list':[str,str,...]}，任务清单
- 人物信息，发送：{'role':str}; 路由：/status；期望接收: {'attribute':dict} #dict的key后端决定,可以包括物质，能量，经验，等级以及其他属性信息
- 背包信息，发送：{'role':str}; 路由：/bag；期望接收：{'equipments':dict} # key为物品名称，value需要统一一下，可以为list或者物品描述
- 技能信息，发送：{'role':str};路由：/skill； 期望接收：{'skills':dict} # key为技能名称，value需要统一一下，可以为list或者技能描述
- 接受某任务，发送：{'text':str, 'role':str}；路由：/accept；期望接收：{'status':bool,''}
- 当前时间，发送：{'role':str}；路由：/time；期望接收：{'time':str} 返回该角色对应的时间
- 其他特殊事件（暂定），发送{'info':str,'role':str,'text':str}，描述任务，并附上玩家输入的text；路由：/others；期望接收：{’role':str,'text':str,'other':str}
- 其它系统，待定