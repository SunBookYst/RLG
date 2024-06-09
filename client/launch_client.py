import requests
import random
import pygame
import json
from copy import deepcopy
# import pygame_textinput
# from hanzi import TextBox
from shared import *

#TODO 显示框实现多种颜色的字体
#TODO 输入角色描述，获取角色像素大头贴
#TODO 根据场景描述，获取场景图象
def render_text(text):
    '''
    渲染一个固定的文本框，暂废弃
    '''
    lines = text.splitlines()
    surfaces = [font.render(line, True, text_color, bg_color) for line in lines]
    return surfaces


def render_text_slide(surface, text, pos, max_width,text_color,font):
    '''
    渲染一个可上下滑动的文本，返回值表示下一个line渲染时开始的位置
    '''
    x, y = pos
    words = list(text)
    for word in words:
        if word == line_break:
            x = 0
            word_surface = font.render(word, True, text_color)
            word_width ,word_height = word_surface.get_size()
            y = y + word_height
            continue
        word_surface = font.render(word, True, text_color)
        word_width, word_height = word_surface.get_size()
        if x + word_width >= max_width:
            x = 0  # reset the x.
            y += word_height  # start on new row.
        surface.blit(word_surface, (x, y))
        x += word_width
    return (x,y)


def render_status(surface): #NOTE 暂时废弃
    surface.fill(box_color)
    fixed_text = "生命值: "
    variable_text = str(LIFE)
    text_surf = font.render(fixed_text, True, fixed_text_color)
    surface.blit(text_surf, (5, 5))
    text_surf = font.render(variable_text, True, variable_text_color)
    surface.blit(text_surf, (35 + text_surf.get_width() + 10, 5))

    fixed_text = "资产: "
    variable_text = str(ASSETS)
    text_surf = font.render(fixed_text, True, fixed_text_color)
    surface.blit(text_surf, (5, 35))
    text_surf = font.render(variable_text, True, variable_text_color)
    surface.blit(text_surf, (15 + text_surf.get_width() + 10, 35))

    fixed_text = "物资: "
    variable_text = str(SUPPLIES)
    text_surf = font.render(fixed_text, True, fixed_text_color)
    surface.blit(text_surf, (5, 65))
    text_surf = font.render(variable_text, True, variable_text_color)
    surface.blit(text_surf, (20 + text_surf.get_width() + 10, 65))

# def render_main_page(screen): #NOTE 暂时废弃
#     screen.fill((50, 50, 50))
#     draw_map(screen, base_bg_image, city_map)
#     # box_x, box_y, box_width, box_height = 1280, 0, 400, 800
#     # pygame.draw.rect(screen, box_color, (box_x, box_y, box_width, box_height))

#     pygame.display.flip()

def render_image(screen):
    global input_text, system_text,main_alpha,vice_alpha,volume
    global main_image, task_image, me_image, system_image
    global changed
    # gray_color = (128, 128, 128, 128)
    screen.fill((0,0,0))
    s_w = screen.get_width()
    s_h = screen.get_height()

    #音乐淡入
    if volume < 1.0:
        volume += 1.0 / (pygame.mixer.get_init()[2] * fade_in_time / 1000)
        pygame.mixer.music.set_volume(volume)


    if current_page == SHOW_MAIN_PAGE:
        main_image.set_alpha(main_alpha)
        if main_alpha<255:
            main_alpha+=20
        image = main_image
    else:
        task_image.set_alpha(vice_alpha)
        if vice_alpha<255:
            vice_alpha+=20
        image = task_image
    i_w , i_h = image.get_size()
    screen.blit(image,(s_w // 2 - i_w // 2, s_h // 2 - i_h // 2))

    gray_surface = pygame.Surface((1270, 300))
    gray_surface.fill((128, 128, 128))  # 设置填充颜色为灰色
    gray_surface.set_alpha(100)
    screen.blit(gray_surface,(10, 580))
    pygame.display.flip()

    if max(main_alpha,vice_alpha)>=255 and volume>=1.0:
        changed = False


def render_dialogue(screen,lines):
    global input_text, system_text,main_alpha,vice_alpha,volume
    global main_image, task_image, me_image, system_image

    if current_role == 0:
        role_image = system_image
    else:
        role_image = me_image

    role_image.set_alpha(max(main_alpha,vice_alpha))
    if current_role == 0:
        screen.blit(role_image,(1000, 300))
        long_text = system_text
    else:
        screen.blit(role_image,(0, 300))
        long_text = input_text

    textbox_rect = pygame.Rect(10, 600, 1250, 280)
    text_surface = pygame.Surface((textbox_rect.width, textbox_rect.height), pygame.SRCALPHA)
    # text_surface = pygame.Surface((textbox_rect.width, textbox_rect.height))
    # text_surface.set_alpha(0)
    # text_surface.fill((50, 50, 50))
    pos = (0, 0)
    lines = [long_text[i:i+w_num] for i in range(0, len(long_text), w_num)]
    for i, line in enumerate(lines[start_line:]):
        pos = render_text_slide(text_surface, line, pos, textbox_rect.width,(255,255,255),main_font)
        if pos[1]>=textbox_rect.width:
            break
    screen.blit(text_surface, (20, 600))
    pygame.display.flip()


def main_menu(screen):
    '''
    开始页面
    加入一个大于屏幕大小的背景图，实现一个碰撞和淡入淡出效果
    '''
    global map_image
    menu = True
    image = map_image
    tmp_font = pygame.font.Font(font_path, 60)
    text = tmp_font.render('开始游戏', True, (245, 245, 245))

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    image_width, image_height = image.get_width(), image.get_height()

    # 图像的初始位置和速度以及淡入信息
    image_x, image_y = 0, 0
    speed_x, speed_y = 1, 1
    alpha = 0
    fade_out=False
    fade_speed=3


    clock = pygame.time.Clock()
    while menu:
        if not fade_out:
            alpha += fade_speed
            if alpha >= 255:
                alpha = 255

        image_x += speed_x
        image_y += speed_y

        if image_x <= 0 or image_x + screen_width >= image_width:
            speed_x = -speed_x
            if image_x<0:
                image_x=0
            if image_x+screen_width>image_width:
                image_x = image_width-screen_width
        if image_y <= 0 or image_y + screen_height >= image_height:
            speed_y = -speed_y
            if image_y<0:
                image_y=0
            if image_y+screen_height>image_height:
                image_y = image_height-screen_height

        screen.fill((0, 0, 0))


        image.set_alpha(alpha)
        text.set_alpha(alpha)

        display_rect = pygame.Rect(image_x, image_y, screen_width, screen_height)
        sub_image = image.subsurface(display_rect)
        screen.blit(sub_image, (0, 0))

        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if screen_width // 2 - text.get_width() // 2 < mouse_x < screen_width // 2 + text.get_width() // 2 and screen_height // 2 - text.get_height() // 2 < mouse_y < screen_height // 2 + text.get_height() // 2:
                        fade_out = True
        # print(fade_out)
        if fade_out == True:
            alpha-=fade_speed
        if alpha<=0:
            menu = False
        clock.tick(FPS)
        pygame.display.update()

def set_menu_1(screen): #TODO补充名字发送函数
    '''
    输入名字
    '''
    global role
    menu = True
    legal = True #名字是否合法
    input_text = ''
    tmp_font = pygame.font.Font(font_path, 40)
    text = tmp_font.render('勇士，现在，告诉我你的名字', True, (245, 245, 245))

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    # 图像的初始位置和速度以及淡入信息
    alpha = 0
    fade_out=False
    fade_speed=3


    clock = pygame.time.Clock()
    while menu:
        if not legal:
            text = tmp_font.render('勇士，你的名字不太合适', True, (245, 245, 245))
            legal = True
        if not fade_out:
            alpha += fade_speed
            if alpha >= 255:
                alpha = 255

        screen.fill((0, 0, 0))
        input_t = tmp_font.render(input_text, True, (245, 245, 245))

        text.set_alpha(alpha)
        input_t.set_alpha(alpha)

        text_rect = text.get_rect(center=(screen_width // 2, (screen_height // 2)-60))
        input_rect = input_t.get_rect(center=(screen_width // 2, (screen_height // 2)))
        screen.blit(text, text_rect)
        screen.blit(input_t, input_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(input_text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", ""))>0:
                        try:
                            role = input_text
                            func = "/legal"
                            r = requests.get(url=url+func,json = {"mode":0,"content":role})
                            r_json = json.loads(r.text)
                            if r_json["status"]!=True:
                                input_text = "你的名字不合适"
                                continue
                        except:
                            continue
                    #TODO 服务端检测名称是否合法，并保存人物名称
                    if False: #默认合法
                        legal = False
                        break
                    menu = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
            elif event.type == pygame.TEXTINPUT:
                input_text += event.text
        if fade_out == True:
            alpha-=fade_speed
        if alpha<=0:
            menu = False
        clock.tick(FPS)
        pygame.display.update()

def set_menu_2(screen):
    '''
    输入名字
    '''
    global role_set
    menu = True
    legal = True #名字是否合法
    input_text = ''
    tmp_font = pygame.font.Font(font_path, 25)
    text = tmp_font.render('然后，告诉我关于你的一切', True, (245, 245, 245))

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    # 图像的初始位置和速度以及淡入信息
    alpha = 0
    fade_out=False
    fade_speed=3


    clock = pygame.time.Clock()
    while menu:
        if not legal:
            text = tmp_font.render('勇士，这不合适', True, (245, 245, 245))
            legal = True
        if not fade_out:
            alpha += fade_speed
            if alpha >= 255:
                alpha = 255

        screen.fill((0, 0, 0))
        input_t = tmp_font.render(input_text, True, (245, 245, 245))

        text.set_alpha(alpha)
        input_t.set_alpha(alpha)

        text_rect = text.get_rect(center=(screen_width // 2, (screen_height // 2)-80))
        input_rect = input_t.get_rect(center=(screen_width // 2, (screen_height // 2)))
        screen.blit(text, text_rect)
        screen.blit(input_t, input_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    role_set = input_text
                    #TODO 服务端检测名称是否合法,并保存人物信息
                    if False: #默认合法
                        legal = False
                        break
                    menu = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
            elif event.type == pygame.TEXTINPUT:
                input_text += event.text
        if fade_out == True:
            alpha-=fade_speed
        if alpha<=0:
            menu = False
        clock.tick(FPS)
        pygame.display.update()

def button_1_function():
    global info_long_text, info_start_line
    info_start_line = 0
    print("按钮1被点击了！")
    func = "/task_info"
    try:
        r = requests.get(url=url+func,json={'role':role})
        r = json.loads(r.text)
        task_list = r['task_list']
    except:
        task_list = ["请求失败，请重试"]
    # task_list = ["帮助市民寻找丢失的小猫","击败盘踞在城镇边缘的强盗团伙","温泉缺水"]
    for i in range(len(task_list)):
        task_list[i] = str(i)+"."+task_list[i]
    info_long_text = line_break.join(task_list)

def button_2_function():
    global info_long_text, info_start_line
    info_start_line = 0
    print("按钮2被点击了！")
    func = "/status"
    try:
        r = requests.get(url=url+func,json={'role':role})
        r = json.loads(r.text)
        attribute = r['attribute']
    except:
        attribute = {"请求失败":"请检查"}
    # attribute = {"龙眼":100,"凤羽":200,"等级":10}
    info_long_text = line_break.join([key+':'+str(attribute[key]) for key in attribute.keys()])

def button_3_function():
    global info_long_text, info_start_line
    info_start_line = 0
    print("按钮3被点击了！")
    func = "/bag"
    try:
        r = requests.get(url=url+func,json={'role':role})
        r = json.loads(r.text)
        equipments = r['equipments']
    except:
        equipments = {"请求失败":"请检查"}
    equipments = {"无锋剑":"平平无奇的铁剑，还未开锋","泻药":"释放给敌人后有概率使其拉肚子","钢铁侠的机甲":"可以发动强力攻击，并使得使用者快速移动"}
    info_long_text = line_break.join([key+':'+str(equipments[key]) for key in equipments.keys()])

def button_4_function():
    global info_long_text, info_start_line
    info_start_line = 0
    print("按钮 4被点击了！")
    func = "/skill"
    try:
        r = requests.get(url=url+func,json={'role':role})
        r = json.loads(r.text)
        skills = r['skills']
    except:
        skills = {"请求失败":"请检查"}
    # skills = {"闭目养神":"通过少许的休息换取少许的体力","温故而知新":"任务后获取的经验值有较大概率额外增加","没轻没重":"攻击时的伤害波动增大"}
    info_long_text = line_break.join([key+':'+str(skills[key]) for key in skills.keys()])


def button_5_function():
    global info_long_text, info_start_line
    info_start_line = 0
    print("按钮 5被点击了！")
    if current_page==SHOW_MAIN_PAGE:
        info_long_text = line_break.join(dialogue_history)
    else:
        info_long_text = line_break.join(vice_history)

def button_6_function(): #测试切换页面功能用
    global current_page,main_alpha,vice_alpha, system_text,volume
    global changed
    global vice_history, dialogue_history
    if current_page == SHOW_MAIN_PAGE:
        current_page =SHOW_VICE_PAGE
        vice_history.append(r['role']+':'+r['text'])
        vice_alpha = 20
        main_alpha = 20
        system_text = "现在在执行任务"*20
        random_item = random.choice([music_file_2,music_file_3])
        volume = 0.0
        changed = True
        pygame.mixer.music.load(random_item)
        pygame.mixer.music.play(-1)
    else:
        current_page = SHOW_MAIN_PAGE
        dialogue_history.append(r['role']+':'+r['text'])
        main_alpha = 20
        vice_alpha = 20
        system_text = "现在回到主界面了"*20
        volume = 0.0
        changed = True
        pygame.mixer.music.load(music_file_1)
        pygame.mixer.music.play(-1)

def button_7_function(num,text,mode): #提交合成资料
    global info_long_text, info_start_line
    print("发送的信息是：",num,text,mode)
    info_start_line = 0
    if num=="":
        num = 0
    else:
        num = int(num)
    print("按钮 7被点击了!")
    func = "/merge"
    try:
        r = requests.get(url=url+func,json={'role':role,'mode':mode,'num':num,'des':text})
        text = r['text']
    except:
        text = "请求失败，请重试"
    # text = "冒出一阵金光，装备合成成功"
    # if current_page==SHOW_MAIN_PAGE:
    info_long_text = text
    # else:
    # long_text = line_break.join(vice_history)

def is_mouse_in_rect(mouse_pos, rect_x, rect_y, rect_width, rect_height):
    if rect_x <= mouse_pos[0] <= rect_x + rect_width and \
       rect_y <= mouse_pos[1] <= rect_y + rect_height:
        return True
    else:
        return False


button_functions = [button_1_function, button_2_function, button_3_function, button_4_function, button_5_function,button_6_function, button_7_function]
buttons = [pygame.Rect(B_x[i], B_y[i], B_w[i], B_h[i]) for i in range(BUTTON_NUM)]

pygame.init()
pygame.mixer.init()
#随着游戏进行图片需要重新加载替换

os.environ["SDL_IME_SHOW_UI"] = "1"
main_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("City Map")
map_image = pygame.image.load(CLIENT_PATH+'./image/map03.png').convert_alpha()
main_image = pygame.image.load(CLIENT_PATH+'./image/bg.png').convert_alpha()
task_image = pygame.image.load(CLIENT_PATH+'./image/task1.png').convert_alpha()
me_image = pygame.image.load(CLIENT_PATH+'./image/me.png').convert_alpha()
system_image = pygame.image.load(CLIENT_PATH+'./image/system.png').convert_alpha()
pygame.mixer.music.load(music_file_1)
pygame.mixer.music.play(-1)

main_menu(main_screen)
#人物名称确定
set_menu_1(main_screen)
#人物设定确定
set_menu_2(main_screen)

changed = True
running = True
main_screen.fill((50, 50, 50))

main_surface = pygame.Surface((1280, 900), pygame.SRCALPHA)
image_surface = pygame.Surface((1280, 900))
dropdown = Dropdown(1280, 640, 320, 40, font, "选择你的合成材料：", ["龙眼", "凤羽"])
num_box = TextBox(1280, 680, 320, 40, font,0)

info_text_surface = pygame.Surface((info_textbox_rect.width, info_textbox_rect.height))
merge_text_surface = pygame.Surface((320, 140))
try:
    func = "/main"
    r =requests.get(url=url+func,json={'role':role,'text':""})
    r = json.loads(r.text)
    system_text = r["text"]
except:
    system_text = "初始通信有误"
clock = pygame.time.Clock()
while running:
    events = pygame.event.get()
    for event in events:
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        if i != 6:
                            button_functions[i]()
                        if i == 6:
                            button_functions[i](num_box.text,merge_long_text,dropdown.selected_num)
                # if is_mouse_in_rect(mouse_pos,des_box.rect.x, des_box.rect.y, des_box.rect.width, des_box.rect.height):
                    # des_box.handle_event(event)
                if is_mouse_in_rect(mouse_pos,num_box.rect.x,num_box.rect.y,num_box.rect.width,num_box.rect.height):
                    num_box.handle_event(event)
                elif is_mouse_in_rect(mouse_pos,dropdown.rect.x,dropdown.rect.y,dropdown.rect.width,dropdown.rect.height):
                    dropdown.handle_event(event)
            elif event.button == 4:  # 滚轮向上
                if is_mouse_in_rect(mouse_pos, 0, 0, 1280, 900):
                    start_line = max(0, start_line - 1)
                elif is_mouse_in_rect(mouse_pos,info_textbox_rect.x,info_textbox_rect.y,info_textbox_rect.width,info_textbox_rect.height):
                    info_start_line = max(0,info_start_line - 1)
                elif is_mouse_in_rect(mouse_pos,merge_textbox_rect.x,merge_textbox_rect.y,merge_textbox_rect.width,merge_textbox_rect.height):
                    merge_start_line = max(0,merge_start_line - 1)
            elif event.button == 5:  # 滚轮向下
                if is_mouse_in_rect(mouse_pos, 0, 0, 1280, 900):
                    start_line = min(len(lines) - textbox_rect.height // line_height, start_line + 1)
                elif is_mouse_in_rect(mouse_pos,info_textbox_rect.x,info_textbox_rect.y,info_textbox_rect.width,info_textbox_rect.height):
                    info_start_line = min(len(info_lines) - info_textbox_rect.height // info_line_height, info_start_line + 1)
                elif is_mouse_in_rect(mouse_pos,merge_textbox_rect.x,merge_textbox_rect.y,merge_textbox_rect.width,merge_textbox_rect.height):
                    merge_start_line = min(len(merge_lines) - merge_textbox_rect.height // merge_line_height, merge_start_line + 1)
            mouse_x, mouse_y = pygame.mouse.get_pos()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if current_role==0:
                    current_role = 1
                else:
                    if current_page==SHOW_MAIN_PAGE:
                        dialogue_history.append(role+":"+input_text)
                        try:
                            r = requests.get(url+"/main",json={'text':input_text,"role":role})
                            r = json.loads(r.text)
                            system_text = r['text']
                            t_role = r["role"]
                            status = r["status"]
                        except:
                            system_text = "请重试"
                            t_role = "请求失败"
                            status = False
                        # r= {}
                        # r['role'] = "systemt_"
                        # r['text'] = "我不听我不听我不听"*10
                        # system_text = r['text']
                        dialogue_history.append(t_role+':'+system_text)
                        #NOTE 从主系统过渡到任务执行状态
                        if status:#TODO 设置触发转换到任务状态的关键词,或者改为其他触发方式，由服务端确认后修改
                            current_page = SHOW_VICE_PAGE
                            vice_history.append(t_role+':'+system_text)
                            vice_alpha = 20
                            main_alpha = 20
                            random_item = random.choice([music_file_2,music_file_3])
                            volume = 0.0
                            changed = True
                            pygame.mixer.music.load(random_item)
                            pygame.mixer.music.play(-1)
                            status = False
                            #TODO 同时为任务生成场景图，存放到用户的./image/文件夹下，同时在render_dialogue处指定被调用的图片
                    if current_page == SHOW_VICE_PAGE:
                        vice_history.append(role+":"+input_text)
                        try:
                            r = requests.get(url+"/feedback",json={'text':input_text,"role":role})
                            r = json.loads(r.text)
                            # system_text = r['text']
                            if r["role"] == None:
                                t_role = "系统"
                            t_role = r["role"]
                            system_text = r["text"]
                            status = r["status"]
                        except:
                            t_role="请求失败"
                            system_text = "请重试"
                            status = False
                            # system_text = "请求失败，请重试"
                        # r= {}
                        # r['role'] = "system"
                        # r['text'] = "我不听我不听我不听"*10
                        # system_text = r['text']
                        # system_text = "开始执行任务"*10
                        vice_history.append(t_role+':'+system_text)
                        if status:#TODO 触发信息设置同上
                            current_page = SHOW_MAIN_PAGE
                            dialogue_history.append(t_role+':'+system_text)
                            main_alpha = 20
                            vice_alpha = 20
                            vice_history = [] #NOTE 任务内对话信息任务结束后不保存
                            volume = 0.0
                            changed = True
                            pygame.mixer.music.load(music_file_1)
                            pygame.mixer.music.play(-1)
                            status = False
                    input_text = ''
                    current_role = 0
            elif event.key == pygame.K_BACKSPACE:
                if is_mouse_in_rect(mouse_pos,10, 600, 1250, 280):
                    input_text = input_text[:-1]
                elif is_mouse_in_rect(mouse_pos,num_box.rect.x, num_box.rect.y,num_box.rect.width,num_box.rect.height):
                    num_box.handle_event(event)
                elif is_mouse_in_rect(mouse_pos,merge_textbox_rect.x,merge_textbox_rect.y,merge_textbox_rect.width,merge_textbox_rect.height):
                    merge_long_text = merge_long_text[:-1]
                # elif is_mouse_in_rect(mouse_pos,des_box.rect.x, des_box.rect.y,des_box.rect.width,des_box.rect.height):
                    # des_box.handle_event(event)
        elif event.type == pygame.TEXTINPUT:
            if is_mouse_in_rect(mouse_pos,10, 600, 1250, 280):
                input_text += event.text
            elif is_mouse_in_rect(mouse_pos,num_box.rect.x, num_box.rect.y,num_box.rect.width,num_box.rect.height):
                num_box.handle_event(event)
            elif is_mouse_in_rect(mouse_pos,merge_textbox_rect.x,merge_textbox_rect.y,merge_textbox_rect.width,merge_textbox_rect.height):
                merge_long_text += event.text
            # elif is_mouse_in_rect(mouse_pos,des_box.rect.x, des_box.rect.y,des_box.rect.width,des_box.rect.height):
                # des_box.handle_event(event)

    if changed:
        render_image(image_surface)

    main_surface.fill((0,0,0,0))# 刷新main_surface
    render_dialogue(main_surface,lines)
    main_screen.blit(image_surface,(0,0))
    main_screen.blit(main_surface,(0,0))


    for i in range(BUTTON_NUM): #渲染右侧按钮
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if B_x[i] <= mouse_x <= B_x[i] + B_w[i] and B_y[i] <= mouse_y <= B_y[i] + B_h[i]:
            pygame.draw.rect(main_screen, B_h_c[i], buttons[i])
        else:
            pygame.draw.rect(main_screen, B_c[i],buttons[i])
        button_text_surface = button_font.render(B_t[i], True, T_c[i])
        button_text_rect = button_text_surface.get_rect(center=buttons[i].center)
        main_screen.blit(button_text_surface, button_text_rect)


    # 渲染右侧信息框
    # info_text_surface = pygame.Surface((info_textbox_rect.width, info_textbox_rect.height))
    info_text_surface.fill((50, 50, 50))
    pos = (0, 0)
    info_lines = [info_long_text[i:i+info_w_num] for i in range(0, len(info_long_text), info_w_num)]
    for i, line in enumerate(info_lines[info_start_line:]):
        pos = render_text_slide(info_text_surface, line, pos, info_textbox_rect.width,(255,255,255),font)
        if pos[1]>=info_textbox_rect.height:
            break

    main_screen.blit(info_text_surface, info_textbox_rect.topleft)

    merge_text_surface.fill((50,50,50))
    m_pos = (0, 0)
    merge_lines = [merge_long_text[i:i+merge_w_num] for i in range(0, len(merge_long_text), merge_w_num)]
    for i, line in enumerate(merge_lines[merge_start_line:]):
        m_pos = render_text_slide(merge_text_surface, line, m_pos, merge_textbox_rect.width,(255,255,255),font)
        if m_pos[1]>=merge_textbox_rect.height:
            break

    main_screen.blit(merge_text_surface, merge_textbox_rect.topleft)

    pygame.draw.rect(main_screen, (255,255,255),pygame.Rect(1280,500,320,20))
    button_text_surface = font.render("          合成描述↓↓↓", True, (0,0,0))
    # button_text_rect = pygame.Rect(1280,620,320,20)
    # merge_text_surface.blit(button_text_surface, button_text_rect)
    main_screen.blit(button_text_surface, (1280,500))
    main_screen.blit(merge_text_surface, (1280,520))

    dropdown.draw(main_screen)
    num_box.draw(main_screen)
    # des_box.draw(main_screen)
    # main_screen.blit(merge_text_surface, merge_textbox_rect.topleft)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
