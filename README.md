# RLG_World

## 介绍

本项目是中国人民大学 高瓴人工智能学院 2024 年春季学期本科生课程《对话系统》最终结课项目。

本系统通过管理不同的大语言模型，构建了一个自由的文字冒险世界，玩家可以在这个世界中自由探索，完成任务，制作装备，学习技能，收集资源，并逐渐揭开这个大陆背后的秘密。

游戏玩法是传统的文字冒险类游戏，你作为玩家，将在【苍穹】大陆上开始属于你自己的冒险，你将通过与各式各样的 NPC 进行对话，挖掘最为隐秘的故事。你可以选择行侠仗义，助人为乐；或者蜗居一角，与世无争；或者努力变强，探索世界；一切的一切，都在这片大陆上，为所有闻名而来的探险者所等待。

## 贡献名单(排名不分先后)
- [SunBookYst](https://github.com/SunBookYst)
- [Jaylen-Lee](https://github.com/Jaylen-Lee)
- [rednight1234](https://github.com/rednight1234)
- [SummerFall1819](https://github.com/SummerFall1819)

## 本地部署
本项目借助了一些开源项目帮助构建。
- [kimi-free-api](https://github.com/LLM-Red-Team/kimi-free-api/tree/master)

    请根据以上网址的指导，自行部署一个 kimi-free-api 服务。

- [Stable Diffusion WebUI](https://github.com/Akegarasu/stable-diffusion-webui)

    请根据以上网址的指导，自行部署一个 stable-diffusion-webui 服务。

在完成上述两个服务器的部署后，分别开启这两个服务器，在默认条件下，其分别会占用本机的 `8000` 端口和 `7860` 端口。
完成后，运行
```bash
cd backend
python app.py
```
其将占用 `5000` 端口，部署一个 Flask 服务器。

在部署完成之后，就可以通过 
```bash
cd client
python launch_client.py
```
启动客户端，游戏主体以 `pygame` 进行表现。

## 后续优化：
- 后端：
    - [ ] 增加异步处理和多线程支持，提升模型反应速度。
    - [ ] 部署速度更快的大语言模型，提升游戏体验。
    - [ ] 增加鲁棒性，提高向前端反馈的稳定性。
    - [ ] 优化游戏架构，细化武器和技能，提供额外接口，对 `Player` 类进行更细致的管理和优化。
    - [ ] 优化代码架构，完善说明文档和注释说明。
    - [ ] 修改 prompt 模板，嵌入长程主线，增加额外的游戏目标。

- 前端：
    - [ ] 优化用户体验，增设按钮等选项，更好面向用户。
    - [ ] 完善美工优化，调整游戏风格。
    - [ ] 迁移至 `streamlit` 以进行多设备、多平台支持。

- 其他
    - [ ] 细化对角色、武器、技能等的相互关系。
    - [ ] 完成点面设计，推进游戏剧情。
    - [ ] 细化世界观设计，增设额外支持。

