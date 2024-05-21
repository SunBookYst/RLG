import pygame
import random
import numpy as np
from collections import deque
from utils import *
from info import *
import copy

map_size_col = 80
map_size_row = 64
road_width = 3
building_size = 2
use_mark = [1,2,3]
# 生成随机地图的代码
def generate_random_map(residential_range, shop_range, k):
    # map_size = 64
    game_map = np.array([[0 for _ in range(map_size_col)] for _ in range(map_size_row)])

    def is_connected(game_map):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        visited = np.array([[False] * map_size_col for _ in range(map_size_row)])

        start = None
        for i in range(map_size_row):
            for j in range(map_size_col):
                if game_map[i][j] in {1, 2, 3}:
                    start = (i, j)
                    break
            if start:
                break

        if not start:
            return False

        queue = deque([start])
        visited[start[0]][start[1]] = True
        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < map_size_row and 0 <= ny < map_size_col and not visited[nx][ny] and game_map[nx][ny] in {1, 2, 3}:
                    visited[nx][ny] = True
                    queue.append((nx, ny))

        for i in range(map_size_row):
            for j in range(map_size_col):
                if game_map[i][j] in {1, 2, 3} and not visited[i][j]:
                    return False
        return True

    def is_valid_road(start, end, existing_roads, k, start_pos,type):
        for s, e,st,t in existing_roads:
            if t!=type:
                continue
            if start_pos==st:
                if not (end < s or start > e):  # If ranges overlap
                    # if abs(start - s) < k or abs(end - e) < k:
                    return False
            elif abs(start_pos-st)<k:
                return False
        return True

    def add_partial_road(horizontal=True, existing_roads=None):
        if existing_roads is None:
            existing_roads = []

        while True:
            # start = random.randint(0, map_size - 1)
            # length = random.randint(map_size // 3, map_size)
            if horizontal:
                start = random.randint(0, map_size_row - 1)
                length = random.randint(map_size_col // 3, map_size_col)
                col_start = random.randint(0, map_size_col - length)
                col_end = col_start + length - 1
                if is_valid_road(col_start, col_end, existing_roads, k,start,0):
                    row = start
                    for col in range(col_start, col_start + length):
                        if game_map[row][col] == 2:
                            game_map[row][col] = 3
                        else:
                            game_map[row][col] = 1
                            if row!=0:
                                game_map[row-1][col] = 3
                            if row!=game_map.shape[0]-1:
                                game_map[row+1][col] = 3
                    existing_roads.append((col_start, col_end,start,0))
                    break
            else:
                start = random.randint(0, map_size_col - 1)
                length = random.randint(map_size_row // 3, map_size_row)
                row_start = random.randint(0, map_size_row - length)
                row_end = row_start + length - 1
                if is_valid_road(row_start, row_end, existing_roads, k,start,1):
                    col = start
                    for row in range(row_start, row_start + length):
                        if game_map[row][col] == 1:
                            game_map[row][col] = 3
                        else:
                            game_map[row][col] = 2
                            if col!=0:
                                game_map[row][col-1] = 3
                            if col!=game_map.shape[1]-1:
                                game_map[row][col+1] = 3
                    existing_roads.append((row_start, row_end,start,1))
                    break
        return existing_roads
    print("正在为城市铺设道路...")
    while True:
        game_map = np.array([[0 for _ in range(map_size_col)] for _ in range(map_size_row)])
        # print("game shape",game_map.shape)
        horizontal_roads = []
        vertical_roads = []

        num_horizontal_roads = random.randint(4, 6)
        num_vertical_roads = random.randint(4, 6)
        for _ in range(num_horizontal_roads):
            horizontal_roads = add_partial_road(horizontal=True, existing_roads=horizontal_roads)

        for _ in range(num_vertical_roads):
            vertical_roads = add_partial_road(horizontal=False, existing_roads=vertical_roads)

        if is_connected(game_map):
            # print("道路违章！")
            break
    def check_zero(matrix):
        for row in matrix:
            for value in row:
                if value != 0:
                    return False
        return True

    def search_round(tmp_game_map,row,col,width,height):
        flag=False
        if row!=0:
            for mark in tmp_game_map[row-1][col:col+width]:
                if mark in use_mark:
                    flag=True
                    break
        if (row+height)<len(tmp_game_map):
            for mark in tmp_game_map[row+height][col:col+width]:
                if mark in use_mark:
                    flag=True
                    break
        if col!=0:
            for mark_list in tmp_game_map[row:row+height]:
                mark = mark_list[col-1]
                if mark in use_mark:
                    flag=True
                    break
        if (col+width)<len(tmp_game_map[0]):
            for mark_list in tmp_game_map[row:row+height]:
                mark = mark_list[col+width]
                if mark in use_mark:
                    flag=True
                    break
        return flag


    def find_adjacent_empty_cells(width,height,mark,round=1):
        tmp_game_map = np.array(game_map)
        empty_cells = []
        for k in range(round):
            for tmp_row in range(map_size_row-height+1):
                for tmp_col in range(map_size_col-width+1):
                    # if (game_map[tmp_row][tmp_col] == 0) and (game_map[row+1][col] == 0) and (game_map[row][col+1] == 0) and (game_map[row+1][col+1] == 0):
                    # for i in range(width):
                    #     col = tmp_col+i
                    #     for j in range(height):
                    #         row = tmp_row+j
                    # row = tmp_row
                    # col = tmp_col
                    # print("0",tmp_game_map)
                    # print("1",tmp_game_map[tmp_row:tmp_row+height,tmp_col:tmp_col+width])
                    if check_zero(tmp_game_map[tmp_row:tmp_row+height,tmp_col:tmp_col+width]) and search_round(tmp_game_map,tmp_row,tmp_col,width,height):
                        # print("2",tmp_game_map[tmp_row:tmp_row+height,tmp_col:tmp_col+width])
                        # if search_round(tmp_game_map,tmp_row,tmp_col,width,height):
                            # print(tmp_row,tmp_col,"lalalal")
                        # if (row > 0 and tmp_game_map[row - 1][col] in {1, 2, 3}) or \
                        # (row < map_size - 1 and tmp_game_map[row + 1][col] in {1, 2, 3}) or \
                        # (col > 0 and tmp_game_map[row][col - 1] in {1, 2, 3}) or \
                        # (col < map_size - 1 and tmp_game_map[row][col + 1] in {1, 2, 3}) or \
                        # (round>1 and (mark in tmp_game_map[max(0,row-height):min(len(tmp_game_map),row+height)][col])): # 垂直方向有建筑物
                        empty_cells.append((tmp_row, tmp_col))
                        for i in range(width):
                            col = tmp_col+i
                            for j in range(height):
                                row = tmp_row+j
                                tmp_game_map[row][col]=mark #某类型建筑物占用
                        # print(tmp_row,tmp_col)
                        # for row in tmp_game_map:
                        #     formatted_row = [f"{x:>3}" for x in row]
                        #     print(' '.join(formatted_row))
                            # print('  '.join(map(str, row)))
        return empty_cells

    residential_count = random.randint(*residential_range)
    print("正在生成建筑...")
    width=3
    height=3
    empty_cells = find_adjacent_empty_cells(width,height,4)
    for _ in range(residential_count):
        if not empty_cells:
            break
        row,col = random.choice(empty_cells)
        game_map[row:row+height,col:col+width] = 40
        game_map[row+height-1][col] = 4

    shop_count = random.randint(*shop_range)
    shop_0_count = random.randint(0,shop_count)
    shop_1_count = shop_count-shop_0_count
    width=3
    height=3
    empty_cells = find_adjacent_empty_cells(width,height,5)
    for _ in range(shop_1_count):
        if not empty_cells:
            break
        row,col = random.choice(empty_cells)
        game_map[row:row+height,col:col+width] = 50
        game_map[row+height-1][col] = 5
    width=4
    height=3
    empty_cells = find_adjacent_empty_cells(width,height,6)
    for _ in range(shop_0_count):
        if not empty_cells:
            break
        row,col = random.choice(empty_cells)
        game_map[row:row+height,col:col+width] = 60
        game_map[row+height-1][col] = 6
    return game_map

# 初始化 Pygame
# pygame.init()
# width, height = 1024, 1024
# # screen = pygame.display.set_mode((width, height))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# pygame.display.set_caption("City Map")

# 随机生成地图
residential_range = (30, 40)
shop_range = (30, 40)
k = 5 # 道路间最小距离
#同方向位置重合的道路的最小距离
#TODO 建筑物也可以生成在其他建筑物的纵向位置
#TODO 建筑物尺寸改为2*2,横向间隔为1
#TODO 道路生成逻辑修改为先生成一条路，由此拓展
#TODO 断头路尽头一定要有建筑物
#TODO UI界面可滑动

#TODO 建筑点击有反应
#TODO 地面铺设更加平滑
#TODO 道路宽度设置为5，即中心线，路和路沿
#TODO 路演加装路灯
#TODO 十字路口加装红绿灯
#TODO 道路根据方向添加活动小车
#TODO 空地增加树木，垃圾桶，

#TODO 路障生成

city_map = generate_random_map(residential_range, shop_range, k)
for row in city_map:
    formatted_row = [f"{x:>3}" for x in row]
    # print(' '.join(formatted_row))

# 将生成的地图绘制到屏幕上
def draw_map(screen, base_bg_image, city_map):
    for row in range(len(city_map)):
        for col in range(len(city_map[0])):
            # if city_map[row][col] == 0:
            tmp = random.choice([brick_0, brick_1, brick_2, brick_3, brick_4, brick_5, brick_6, brick_7, brick_8])
            tmp = brick_4
            x, y = col * 16, row * 16
            screen.blit(base_bg_image, (x, y), tmp)

    for row in range(len(city_map)):
        for col in range(len(city_map[0])):
            if city_map[row][col] in {1, 2, 3}:
                if city_map[row][col] == 1:
                    tmp = road_0
                elif city_map[row][col] == 2:
                    tmp = road_1
                else:
                    tmp = road_x
                x, y = col * 16, row * 16
                screen.blit(base_bg_image, (x, y), tmp)

    tag = 0
    for row in range(len(city_map)): #建筑应当自上而下叠加
        for col in range(len(city_map[0])):
            if city_map[row][col] in {4, 5, 6}:
                if city_map[row][col] == 4:
                    tag = 4
                    tmp = random.choice([house_0, house_1, house_2])
                elif city_map[row][col] == 5:
                    tag = 5
                    tmp = random.choice([shop_1])
                elif city_map[row][col] == 6:
                    tag = 6
                    tmp = random.choice([shop_0])
                # city_map[row][col]=0
                # city_map[row+1][col]=0
                # city_map[row][col+1]=0
                # city_map[row+1][col+1]=0
                # print(tag,tmp.height,tmp.width)
                x = col * 16
                y = row* 16-tmp.height+48
                if tag==5 or tag==6:
                    y = y-32
                # print(x,y)
                # x,y = col*16, row*16
                screen.blit(base_bg_image, (x, y), tmp)
    # tag = 0
    # for row in range(len(city_map)): #建筑应当自上而下叠加
    #     for col in range(len(city_map[0])):
    #         if city_map[row][col] in {4, 5, 6}:
    #             if city_map[row][col] == 4:
    #                 tag = 4
    #                 tmp = random.choice([house_0, house_1, house_2])
    #             elif city_map[row][col] == 5:
    #                 tag = 5
    #                 tmp = random.choice([shop_1])
    #             elif city_map[row][col] == 6:
    #                 tag = 6
    #                 tmp = random.choice([shop_0])
    #             # city_map[row][col]=0
    #             # city_map[row+1][col]=0
    #             # city_map[row][col+1]=0
    #             # city_map[row+1][col+1]=0
    #             print(tag,tmp.height,tmp.width)
    #             x = col * 16
    #             y = row* 16-tmp.height+48
    #             if tag==5:
    #                 y = y-32
    #             print(x,y)
    #             # x,y = col*16, row*16
    #             screen.blit(base_bg_image, (x, y), tmp)
if __name__ =="__main__":
    pygame.init()
    width, height = 1024, 1024
    # screen = pygame.display.set_mode((width, height))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("City Map")
    running = True
    screen.fill((0, 0, 0))
    draw_map(screen, base_bg_image, city_map)
    box_x, box_y, box_width, box_height = 1024, 0, 600, 800
    # console_output = io.StringIO()
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_width, box_height))
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # screen.fill((0, 0, 0))
        # draw_map(screen, base_bg_image, city_map)
        # pygame.display.flip()

    pygame.quit()