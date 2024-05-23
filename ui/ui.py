import random

import pygame

from map import *
from utils import *
from info import *
from button import *

def render_main_page(screen):
    screen.fill((50, 50, 50))
    draw_map(screen, base_bg_image, city_map)
    box_x, box_y, box_width, box_height = 1280, 0, 400, 800
    # console_output = io.StringIO()
        # 绘制方框
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_width, box_height))

    # 获取控制台输出的内容
    console_output.seek(0)
    console_text = console_output.read()
    console_output.seek(0)
    console_output.truncate(0)

    # 渲染并绘制文本
    text_surfaces = render_text(console_text)
    for i, surface in enumerate(text_surfaces):
        screen.blit(surface, (box_x + 5, box_y + 5 + i * (font.get_linesize() + 2)))
    # status_surface = pygame.Surface((400, 300))
    # render_status(status_surface)
    # screen.blit(status_surface, (1280, 400))
    pygame.display.flip()

def render_second_page(screen):
    # 在第二个页面显示不同的内容
    screen.fill((50,50,50))
    text = "这是第二个页面"
    text_surfaces = render_text(text)
    for i, surface in enumerate(text_surfaces):
        screen.blit(surface, (box_x + 5, box_y + 5 + i * (font.get_linesize() + 2)))




# TODO 项目主角包括 势力，地图背景，地点，事件，展示板，属性版
# TODO 资源包括 音乐，音效
# TODO 事件发生标识
# print("你好")
pygame.init()
width, height = 1280, 1024
# screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("City Map")
# font_path = "C:\Windows\Fonts\simhei.ttf"  # 请确保路径正确
# font = pygame.font.Font(font_path, 20)

running = True
screen.fill((50, 50, 50))
# draw_map(screen, base_bg_image, city_map)
# box_x, box_y, box_width, box_height = 1024, 0, 600, 800
# # console_output = io.StringIO()
#     # 绘制方框
# pygame.draw.rect(screen, box_color, (box_x, box_y, box_width, box_height))

# # 获取控制台输出的内容
# console_output.seek(0)
# console_text = console_output.read()
# console_output.seek(0)
# console_output.truncate(0)

# # 渲染并绘制文本
# text_surfaces = render_text(console_text, font, text_color, box_color)
# for i, surface in enumerate(text_surfaces):
#     screen.blit(surface, (box_x + 5, box_y + 5 + i * (font.get_linesize() + 2)))
#TODO 设定FPS，保存页面状态
main_surface = pygame.Surface((1920, 1024))
second_surface = pygame.Surface((1920, 1024))
status_surface = pygame.Surface((400, 300))
render_main_page(main_surface)
render_status(status_surface)
render_second_page(second_surface)
pygame.display.flip()
first_draw = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                # 切换页面状态
                if current_page == SHOW_MAIN_PAGE:
                    current_page = SHOW_SECOND_PAGE
                else:
                    current_page = SHOW_MAIN_PAGE
    matter = False
    if current_page == SHOW_MAIN_PAGE:
        screen.blit(main_surface,(0,0))
        screen.blit(status_surface, (1280, 400))
    else:
        screen.blit(second_surface,(0,0))
    draw_button(screen, "切换页面", button_x, button_y, button_width, button_height, button_color, button_hover_color,font,text_color)
    # screen.fill((0, 0, 0))
    # draw_map(screen, base_bg_image, city_map)
    pygame.display.flip()

pygame.quit()
