import sys
import io
import os
import pygame

pygame.init()

CLIENT_PATH = os.path.split(os.path.realpath(__file__))[0]
base_bg_image = pygame.image.load(CLIENT_PATH+'/asset/CP_V1.0.4.png')


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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class TextBox:
    def __init__(self, x, y, w, h, font,mode):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.font = font
        self.text = ""
        self.active = False
        self.mode = mode

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 如果单击文本框，则激活它
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
        if event.type == pygame.TEXTINPUT and self.active:
            if self.mode==1:
                self.text += event.text
            else:
                if event.text.isdigit():
                    self.text += event.text
                else:
                    self.text = self.text

    def draw(self, screen):
        # 绘制文本框
        pygame.draw.rect(screen, self.color, self.rect, 3 if self.active else 1)
        # 渲染文本
        text_surf = self.font.render(self.text, True, WHITE)
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))
        # pygame.draw.rect(screen, BLACK, self.rect, 2)

class Dropdown:
    def __init__(self, x, y, w, h, font, main, options):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.font = font
        self.main = main
        self.options = options
        self.selected = options[0]
        self.selected_num = 0
        self.expanded = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.main+self.selected, True, BLACK)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

        # if self.expanded:
        #     for i, option in enumerate(self.options):
        #         option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
        #         pygame.draw.rect(screen, GRAY if i % 2 == 0 else WHITE, option_rect)
        #         option_surf = self.font.render(option, True, BLACK)
        #         screen.blit(option_surf, option_surf.get_rect(center=option_rect.center))

    def handle_event(self, event): #FIXME 切换成循环切换的逻辑会更好
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # self.expanded = not self.expanded
                if self.selected_num==0:
                    self.selected_num=1
                    self.selected = "凤羽"
                else:
                    self.selected_num=0
                    self.selected = "龙眼"
            # elif self.expanded:
            #     for i, option in enumerate(self.options):
            #         option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
            #         if option_rect.collidepoint(event.pos):
            #             self.selected = option
            #             self.selected_num = i
            #             self.expanded = False
            #             break
            #     else:
            #         self.expanded = False


map_size_col = 80
map_size_row = 64

font_path = "C:\Windows\Fonts\simhei.ttf" #FIXME
font = pygame.font.Font(font_path, 20)
main_font = pygame.font.Font(font_path,25)
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
SHOW_VICE_PAGE = 1
current_page = SHOW_MAIN_PAGE

# buttons
BUTTON_NUM = 7
B_i = [""]
B_t = ["任务","属性","背包","技能","历史","测试","提交"] # box text
B_x = [1280,1360,1440,1520,1280,1360,1440]
B_y = [740,740,740,740,820,820,820]
B_w = [80,80,80,80,80,80,80] # box weight
B_h = [80,80,80,80,80,80,80] # box height
B_h_c = [(140,140,140),(140,140,140),(140,140,140),(140,140,140),(140,140,140),(140,140,140),(140,140,140)] # box hover color
B_c = [(190,190,190),(190,190,190),(190,190,190),(190,190,190),(190,190,190),(190,190,190),(190,190,190)] # box color
T_c = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)] # text color

music_file_1 = CLIENT_PATH + "\sound\Pixel Parade.mp3"
music_file_2 = CLIENT_PATH + "\sound\Pixel Battle.mp3"
music_file_3 = CLIENT_PATH + "\sound\Pixel Battle2.mp3"


FPS=45 #全局帧率
screen_width, screen_height = 1280, 720 #替换为获取
# long_text = "这是一个示例文本。" * 200 #用于填充 信息 板块
# long_text_merge = "这是一个示例"*10
# dropdown = Dropdown(100, 50, 200, 40, font, "选择一个选项", ["选项1", "选项2", "选项3"])
url = "http://10.46.47.169:5000"#TODO 服务端url地址
role = '' #TODO 在初始界面确定角色名称，服务端检测，禁止重名
role_set = ''
scene = 0 #0 为主界面， 1为执行任务时的交互界面
line_break = "#"

input_text = ''
system_text = '欢迎来到这个世界'*10
dialogue_history = ["system:欢迎来到这里"]
vice_history = ["system:开始执行任务xxx"]
#音乐相关
volume = 0.0
fade_in_time = 3000  # 3 秒淡入

#NOTE 主界面文本框
current_role = 0 # 0表示对方，1表示自己
line_height = main_font.get_linesize()
textbox_rect = pygame.Rect(0,0,1280,320)
start_line = 0
scroll_offset = 0 #NOTE 主界面滚轴偏移量
w_num = textbox_rect.width//(line_height-2)
lines = []
main_alpha = 20

#NOTE 执行任务文本框,其余与主界面共用变量
vice_offset = 0
vice_alpha = 20

#NOTE 右侧info框
info_long_text = "这是一个示例文本。" * 200
info_line_height = font.get_linesize()
info_textbox_rect = pygame.Rect(1280, 0, 320, 500)
info_scroll_offset = 0 #NOTE info界面滚轴偏移量
info_start_line = 0
info_w_num = info_textbox_rect.width//(info_line_height-2)
info_lines = []
pos = (0, 0) # 渲染info文字使用的变量

merge_long_text = ""
merge_textbox_rect = pygame.Rect(1280, 520, 320, 120)
merge_line_height = font.get_linesize()
merge_start_line = 0
merge_w_num = merge_textbox_rect.width//(merge_line_height-2)
