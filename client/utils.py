import pygame
import sys
import io

pygame.init()
size = width, height = 400,300
screen = pygame.display.set_mode(size)
base_bg_image = pygame.image.load('./asset/CP_V1.0.4.png')
# brick，road，house，car，others
rect = base_bg_image.get_rect()
width = rect.width
height = rect.height
bgcolor = pygame.Color('white')
shop_0 = pygame.Rect(16,height-896+48,64,48)
shop_1 = pygame.Rect(112,height-896+48,48,48)
shop_2 = pygame.Rect(192,height-896+40,64,56)

house_0 = pygame.Rect(32,height-896-96,48,128)
house_1 = pygame.Rect(112,height-896-96,48,128)
house_2 = pygame.Rect(192,height-896-96,48,128)
house_3 = pygame.Rect(272,height-896-96,80,128)


road_0 = pygame.Rect(80,608,16,16)
road_1 = pygame.Rect(112,608,16,16)
road_x = pygame.Rect(48,608,16,16)

brick_0 = pygame.Rect(400,784,16,16)
brick_1 = pygame.Rect(432,784,16,16)
brick_2 = pygame.Rect(464,784,16,16)
brick_3 = pygame.Rect(400,816,16,16)
brick_4 = pygame.Rect(432,816,16,16)
brick_5 = pygame.Rect(464,816,16,16)
brick_6 = pygame.Rect(400,848,16,16)
brick_7 = pygame.Rect(432,848,16,16)
brick_8 = pygame.Rect(464,848,16,16)
fclock = pygame.time.Clock()

font_path = "C:\Windows\Fonts\simhei.ttf"
font = pygame.font.Font(font_path, 20)
button_font = pygame.font.Font(font_path, 25)
text_color = (255, 255, 255)
bg_color = (50, 50, 50)
box_color = (50, 50, 50)
fixed_text_color = (0, 255, 0)
variable_text_color = (192, 192, 192)
box_x, box_y, box_width, box_height = 1280, 0, 400, 800

# attributes
LIFE = 100
ASSETS = 5000
SUPPLIES = 300

SHOW_MAIN_PAGE = 0
SHOW_SECOND_PAGE = 1
current_page = SHOW_MAIN_PAGE

# buttons
BUTTON_NUM = 4
B_i = [""]
B_t = ["任务","属性","背包","技能"] # box text
B_x = [1280,1360,1440,1520]
B_y = [600,600,600,600]
B_w = [80,80,80,80] # box weight
B_h = [80,80,80,80] # box height
B_h_c = [(140,140,140),(140,140,140),(140,140,140),(140,140,140)] # box hover color
B_c = [(190,190,190),(190,190,190),(190,190,190),(190,190,190)] # box color
T_c = [(0,0,0),(0,0,0),(0,0,0),(0,0,0)] # text color