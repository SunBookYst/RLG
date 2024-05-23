import random
import pygame
import numpy as np
from collections import deque

from shared import *

residential_range = (30, 40) #居民楼生成数量范围
shop_range = (30, 40) #商店生成数量范围
num_horizontal_roads = random.randint(4, 6) #道路生成数量
num_vertical_roads = random.randint(4, 6)
k = 5 # 道路间最小距离
use_mark = [1,2,3] #标记道路

def generate_random_map(residential_range, shop_range, k):
    game_map = np.array([[0 for _ in range(map_size_col)] for _ in range(map_size_row)])

    def is_connected(game_map):
        '''
        判断最后生成的道路是否全联通，否则重新生成道路
        '''
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
        '''
        start end 道路起止的纵/横坐标，
        existing_road，现存所有道路
        k 最小道路间距
        start_pos 横向道路所在行，或纵向道路所在列
        type 横向/纵向道路
        验证逻辑：和已有道路冲突则废弃；冲突标准：与已有道路区间重合的情况下，间距未达到k。若区间未重合，例如横向道路区间分别为（1，10）和（20，30），则不会冲突
        '''
        for s, e,st,t in existing_roads:
            if t!=type:
                continue
            if start_pos==st:
                if not (end < s or start > e):  # If ranges overlap
                    return False
            elif abs(start_pos-st)<k:
                return False
        return True

    def add_partial_road(horizontal=True, existing_roads=None):
        '''
        增加纵向/横向道路，通过is_valid_road验证是否合法
        '''
        if existing_roads is None:
            existing_roads = []

        while True:
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
                            if row!=0: #在此实现宽为3的路
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
                            if col!=0: #在此实现宽为3的路
                                game_map[row][col-1] = 3
                            if col!=game_map.shape[1]-1:
                                game_map[row][col+1] = 3
                    existing_roads.append((row_start, row_end,start,1))
                    break
        return existing_roads
    print("正在为城市铺设道路...")
    while True:
        game_map = np.array([[0 for _ in range(map_size_col)] for _ in range(map_size_row)])
        horizontal_roads = []
        vertical_roads = []

        for _ in range(num_horizontal_roads):
            horizontal_roads = add_partial_road(horizontal=True, existing_roads=horizontal_roads)

        for _ in range(num_vertical_roads):
            vertical_roads = add_partial_road(horizontal=False, existing_roads=vertical_roads)

        if is_connected(game_map):
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
        '''
        width、height 建筑宽高
        mark 建筑类型
        round 废弃参数

        寻找路旁可建筑区域
        '''
        tmp_game_map = np.array(game_map)
        empty_cells = []
        for k in range(round):
            for tmp_row in range(map_size_row-height+1):
                for tmp_col in range(map_size_col-width+1):
                    if check_zero(tmp_game_map[tmp_row:tmp_row+height,tmp_col:tmp_col+width]) and search_round(tmp_game_map,tmp_row,tmp_col,width,height):
                        empty_cells.append((tmp_row, tmp_col))
                        for i in range(width):
                            col = tmp_col+i
                            for j in range(height):
                                row = tmp_row+j
                                tmp_game_map[row][col]=mark #某类型建筑物占用
        return empty_cells

    residential_count = random.randint(*residential_range)
    print("正在生成建筑...")
    # 居民楼的宽高信息
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
    #一种商店的宽高信息
    width=3
    height=3
    empty_cells = find_adjacent_empty_cells(width,height,5)
    for _ in range(shop_1_count):
        if not empty_cells:
            break
        row,col = random.choice(empty_cells)
        game_map[row:row+height,col:col+width] = 50
        game_map[row+height-1][col] = 5
        #一种商店的宽高信息
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

city_map = generate_random_map(residential_range, shop_range, k)

# for row in city_map:
#     formatted_row = [f"{x:>3}" for x in row]
    # print(' '.join(formatted_row)) #NOTE 输出字符格式的地图，如有需要可以解除此处注释

#TODO 建筑点击有反应
#TODO 地面铺设更加平滑
#TODO 道路宽度设置为5，即中心线，路和路沿
#TODO 路演加装路灯
#TODO 十字路口加装红绿灯
#TODO 道路根据方向添加活动小车
#TODO 空地增加树木，垃圾桶，
#TODO 路障生成

def draw_map(screen, base_bg_image, city_map):
    '''
    绘制地图到屏幕，由地基到建筑，由上到下，依次绘制
    '''
    for row in range(len(city_map)):
        for col in range(len(city_map[0])):
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
    for row in range(len(city_map)):
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
                x = col * 16
                y = row* 16-tmp.height+48
                if tag==5 or tag==6: #位置修正
                    y = y-32
                screen.blit(base_bg_image, (x, y), tmp)