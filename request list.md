Request List

- 主界面交互，发送:{'text':str,'role':str}; 路由：/main ; 期望接收：{'text':str,'role':str，'status':bool, subimg:base64 :Null},'role'默认为系统, status判断是否切换入任务系统，若非判断成功接收到任务，则一直返回False
- 子任务交互信息，发送：{'text': str, 'role': str，'items':[str,str,...],'skills':[str,str,...],'roles':[str,str,...]}，即我的输入；路由：/feedback；期望接收：{'text':str,'role':str，'status':bool, npc_status: bool, image_data: base64/None} ，即与我交互的角色的反馈,status判断任务是否结束，若结束返回True; items表示本次使用的物品，skills表示本次会使用到的技能，roles表示本次任务历史上出现过的角色; npc_status表示是否是新角色，若是则在image_data中加入角色头像

- 登录发送信息已更新ip地址 发送{'email':str,'password':str,'ip':str},前者为注册用的邮箱地址，后者为加密后的密码,ip为此次登录使用的ip地址和端口，用于系统向本地发送消息 ； 期望接收{'status_code':int,'username':str},username为注册时的用户名，status_code 200表示成功，其他还有如密码不正确，未注册等错误； 路由 /login

- 注册 发送{'email':str,'username':str,'password':str,'ip':str},email和password同上，需要注意username需要检测合法性； 期望接收 {'status_code':int},200为注册成功，其他code自定义，例如重名，邮箱已被使用，名称不合法等等；密码加密操作在前端完成；ip为玩家IP地址以及端口 路由/signup

- 请求生成新的任务 发送:{'text':str,'role':str}; 路由：/task_request ; 期望接收：{'text':str,'role',str},和DM对话的返回内容格式一致
- 请求查看个性化任务列表 同查看任务列表, 路由为 task_info_personal,
- 选择任务/个性化任务的select和select_personal两个路由, 发送{'role':str,'task_name':str},返回{'image_data':base64，'text':str}，imamge_data为任务背景图，text为进入任务后收到的第一句话

- 发起挑战 发送 {'role1':str,'role2':str,'image_data'},role1是发起者，role2是被挑战者，image_data是发起挑战者的头像，需要发送给被挑战者，返回{'status_code':int，'status':bool,'image_data':base64,'id':str},分别是，status_code检测发送信息是否正确（如被挑战这是否存在，是否在线等，有可能因为前后端在线信息不同步导致错误），正确则返回200，status被挑战者是否接受挑战,若接受挑战image_data返回base64数据，否则为None，id为本次对战id，路由为/challenge
- 接受挑战 {"role":str,'id':str},id表示对战的id，系统返回{'status_code':int},状态码200表示正常发出（意外情况，接受挑战之前被挑战者就下线了）
- 拒绝挑战{"role":str,'id':str},id表示对战的id，系统返回{'status_code':int}，状态码200表示正常发出
- 玩家客户端接收信息路由/challenge_info，其中ip信息随登录信息一起发送，可能会随每次登陆而不同，因此服务器需要在玩家登陆后更新这一信息, 期待服务器发送格式{'id':str,'role':str，'image_data':str},其中id为服务器生成的本次挑战的id，与返回给挑战发起者的一样，role为挑战发起者,image_data为挑战发起者的头像。返回服务器格式{'status':bool,'id':str,'image_data':base64},status为是否接受此次挑战，id为本次挑战的ip，image_data为被挑战者的头像
- 对战中对话 {"role":str,"id":str,'text':str,'items':[],'skills':[]},id为本次对战id; 返回{'role':str,'action':str,'result':str},action为对方动作，result为系统判定结果 路由为/battle
- 获取在线玩家列表 {'role':str},发送用户名；返回{"roles":[str,str,...]}返回用户列表 路由/get_list

- 刷新接口 用于发送在线情况和处理挑战信息，发送{"role":str},ip为用户拒绝/接收的挑战ip，ip_status是用户接收/拒绝挑战，一旦超过指定时间没有发送该刷新信息，系统就判定该用户已经不在线，获取的信息包括{"id_list":[str,str,...],"role_list":[str,str,...],"accpec_id":[str,str,...]},表示此用户收到的别人发起的挑战的id、发起者名字,两者一一对应，还有一个在刷新时间内被接受的挑战列表；被接受挑战会顺序选取第一个，其他则通过下面的接口返回False来挤掉 路由/refrash
- 接受挑战，设定该路由而不是整合到刷新接口的目的是，避免出现接受挑战后，对方因为等待而不在线/进入了其他挑战等不可用情况，发送信息{"id":str,"status":bool},id是挑战id，status是接受用户的反馈， 返回信息{"status":bool},即对方是否可以进入该挑战（若可以进入则对方自动进入该挑战），返回为True之后该用户才进入挑战对话页面（若发送false则直接返回false） 路由/accept_c

# 一些可能出现的状况，被挑战者接受挑战之前挑战者就下线了

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