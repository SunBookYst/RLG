# import requests
# import re
import pygame
from map import *

FPS=60 #全局帧率
long_text = "这是一个示例文本。" * 200 #用于填充 信息 板块
url = "xxx"#TODO 服务端url地址


def render_text(text):
    '''
    渲染一个固定的文本框，暂废弃
    '''
    lines = text.splitlines()
    surfaces = [font.render(line, True, text_color, bg_color) for line in lines]
    return surfaces


def render_text_slide(surface, text, pos, max_width,text_color):
    '''
    渲染一个可上下滑动的文本，返回值表示下一个line渲染时开始的位置
    '''
    x, y = pos
    words = list(text)
    for word in words:
        word_surface = font.render(word, True, text_color)
        word_width, word_height = word_surface.get_size()
        if x + word_width >= max_width:
            x = 0  # reset the x.
            y += word_height  # start on new row.
        surface.blit(word_surface, (x, y))
        x += word_width
    return (x,y)


def render_status(surface):
    '''
    暂废弃
    '''
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

def render_main_page(screen): #TODO 待替换为与系统文字交互的页面
    screen.fill((50, 50, 50))
    draw_map(screen, base_bg_image, city_map)
    box_x, box_y, box_width, box_height = 1280, 0, 400, 800
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_width, box_height))

    pygame.display.flip()

def render_second_page(screen): #TODO 待替换为过场动画页面
    # 在第二个页面显示不同的内容
    screen.fill((50,50,50))
    text = "这是第二个页面"
    text_surfaces = render_text(text)
    for i, surface in enumerate(text_surfaces):
        screen.blit(surface, (box_x + 5, box_y + 5 + i * (font.get_linesize() + 2)))

def main_menu(screen):
    '''
    开始页面
    加入一个大于屏幕大小的背景图，实现一个碰撞和淡入淡出效果
    '''
    menu = True
    image = pygame.image.load(CLIENT_PATH+'./image/map03.png').convert_alpha()
    tmp_font = pygame.font.Font(font_path, 40)
    text = tmp_font.render('开始游戏', True, (255, 255, 255))

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    image_width, image_height = image.get_width(), image.get_height()

    # 图像的初始位置和速度以及淡入信息
    image_x, image_y = 0, 0
    speed_x, speed_y = 0.5, 0.5
    alpha = 0
    fade_out=False
    fade_speed=1


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

def button_1_function(): # TODO 改为通信，然后将通信结果返回到long_text反馈到信息框
    global long_text, start_line
    start_line = 0
    print("按钮1被点击了！")
    long_text = "按钮一被点击了"*100

def button_2_function():
    global long_text, start_line
    start_line = 0
    print("按钮2被点击了！")
    long_text = "按钮 2被点击了"*100

def button_3_function():
    global long_text, start_line
    start_line = 0
    print("按钮3被点击了！")
    long_text = "按钮3bei点击了"*100

def button_4_function():
    global long_text, start_line
    start_line = 0
    print("按钮 4被点击了！")
    long_text = "按钮4 被点击了"*100


button_functions = [button_1_function, button_2_function, button_3_function, button_4_function]
buttons = [pygame.Rect(B_x[i], B_y[i], B_w[i], B_h[i]) for i in range(BUTTON_NUM)]


pygame.init()
width, height = 1280, 1024
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("City Map")

main_menu(screen)

running = True
screen.fill((50, 50, 50))


main_surface = pygame.Surface((1920, 1024)) #TODO 替换为交互信息
second_surface = pygame.Surface((1920, 1024)) #TODO 替换为需要淡入淡出的图像
render_main_page(main_surface)
render_second_page(second_surface)


# 右侧信息框
line_height = font.get_linesize()
textbox_rect = pygame.Rect(1280, 0, 320, 600)
start_line = 0
w_num = textbox_rect.width//(line_height-2)
pos = (0,0)
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        button_functions[i]()
            elif event.button == 4:  # 滚轮向上
                start_line = max(0, start_line - 1)
            elif event.button == 5:  # 滚轮向下
                start_line = min(len(lines) - textbox_rect.height // line_height, start_line + 1)
            mouse_x, mouse_y = pygame.mouse.get_pos()

    matter = False
    if current_page == SHOW_MAIN_PAGE:
        screen.blit(main_surface,(0,0))
    else:
        screen.blit(second_surface,(0,0))

    for i in range(BUTTON_NUM):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if B_x[i] <= mouse_x <= B_x[i] + B_w[i] and B_y[i] <= mouse_y <= B_y[i] + B_h[i]:
            pygame.draw.rect(screen, B_h_c[i], buttons[i])
        else:
            pygame.draw.rect(screen, B_c[i],buttons[i])
        button_text_surface = button_font.render(B_t[i], True, T_c[i])
        button_text_rect = button_text_surface.get_rect(center=buttons[i].center)
        screen.blit(button_text_surface, button_text_rect)

    text_surface = pygame.Surface((textbox_rect.width, textbox_rect.height))
    text_surface.fill((50, 50, 50))
    pos = (0,0)
    lines = [long_text[i:i+w_num] for i in range(0, len(long_text), w_num)]
    for i, line in enumerate(lines[start_line:]):
        pos = render_text_slide(text_surface, line, pos, textbox_rect.width,(255,255,255))
        if pos[1]>=textbox_rect.height:
            break
    screen.blit(text_surface, textbox_rect.topleft)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
