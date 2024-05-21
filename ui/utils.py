import pygame

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
# fps = 5
# test = road_0
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:           # 处理退出事件
#             running = False
#     screen.fill(bgcolor)                #设置背景的颜色
#     # row=frameNum//4                     #求整数商为行号，根据frameNum改变：0，1
#     # col=frameNum%4                      #求余数为列号，根据frameNum改变：0，1，2，3，
#     # rect2.x=col*rect2.width             #rect2是blit方法第3个参数，             
#     # rect2.y=row*rect2.height            #根据frameNum改变,从image取不同帧
#     # if direction==0:
#     screen.blit(base_bg_image, (0, 0),test) #在屏幕指定位置绘制图形
#     pygame.display.flip()               #刷新游戏场景    
#     fclock.tick(fps)
    # else:                               #不知反转图像是否还有其它更好的方法
        # p = pygame.Surface((rect2.width, rect2.height))    #创建一个Surface实例
        # p.blit(base_bg_image, (0, 0), test)    #从image中拷贝rect2区域图像到p,左上角对齐
        # p=pygame.transform.flip(p,True,False)#  反向
        # p.convert_alpha()              #加此条语句后不能去掉背景
        # p.set_colorkey(BLACK)           #去图像背景，不理想
        # screen.blit(p, (x, 60))