import pygame
import random
from collections import deque
from utils import *

# 生成随机地图的代码
def generate_random_map(residential_range, shop_range, k):
    map_size = 64
    road_width = 3
    building_size = 2
    game_map = [[0 for _ in range(map_size)] for _ in range(map_size)]

    def is_within_bounds(x, y):
        return 0 <= x < map_size and 0 <= y < map_size

    def is_connected(game_map):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        visited = [[False] * map_size for _ in range(map_size)]

        start = None
        for i in range(map_size):
            for j in range(map_size):
                if game_map[i][j] in {1, 2, -1}:
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
                if is_within_bounds(nx, ny) and not visited[nx][ny] and game_map[nx][ny] in {1, 2, -1}:
                    visited[nx][ny] = True
                    queue.append((nx, ny))

        for i in range(map_size):
            for j in range(map_size):
                if game_map[i][j] in {1, 2, -1} and not visited[i][j]:
                    return False
        return True

    def add_partial_road():
        direction = random.choice(['horizontal', 'vertical'])
        if direction == 'horizontal':
            row = random.randint(0, map_size - 1)
            col_start = random.randint(0, map_size - 1 - road_width)
            col_end = min(map_size - 1, col_start + road_width)
            for col in range(col_start, col_end + 1):
                game_map[row][col] = 1
        else:
            col = random.randint(0, map_size - 1)
            row_start = random.randint(0, map_size - 1 - road_width)
            row_end = min(map_size - 1, row_start + road_width)
            for row in range(row_start, row_end + 1):
                game_map[row][col] = 2

    def generate_roads():
        for _ in range(random.randint(map_size // 2, map_size)):
            add_partial_road()

    while True:
        game_map = [[0 for _ in range(map_size)] for _ in range(map_size)]
        generate_roads()
        if is_connected(game_map):
            break

    def find_adjacent_empty_cells():
        empty_cells = []
        for row in range(map_size):
            for col in range(map_size):
                if game_map[row][col] == 0:
                    for dy in range(-building_size + 1, building_size):
                        for dx in range(-building_size + 1, building_size):
                            if is_within_bounds(row + dy, col + dx):
                                if game_map[row + dy][col + dx] in {1, 2, -1}:
                                    empty_cells.append((row, col))
                                    break
        return empty_cells

    def add_buildings(building_type, count_range):
        count = random.randint(*count_range)
        for _ in range(count):
            empty_cells = find_adjacent_empty_cells()
            if not empty_cells:
                break
            row, col = random.choice(empty_cells)
            for dx in range(building_size):
                for dy in range(building_size):
                    if is_within_bounds(row + dy, col + dx):
                        game_map[row + dy][col + dx] = building_type

    add_buildings(3, residential_range)  # 添加居民楼
    add_buildings(4, shop_range)  # 添加商店

    return game_map

# 初始化 Pygame
pygame.init()
width, height = 1024, 1024
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("City Map")

# 假设加载了一个背景图像
# base_bg_image = pygame.Surface((16, 16))  # 创建一个16x16的surface作为基础图像
# 在实际使用中，您需要加载真实的图像
# base_bg_image = pygame.image.load('path_to_your_image.png')

# 定义素材位置
# shop_0 = pygame.Rect(16, height-896+48, 64, 48)
# shop_1 = pygame.Rect(112, height-896+48, 48, 48)
# shop_2 = pygame.Rect(192, height-896+40, 64, 56)

# house_0 = pygame.Rect(32, height-896-96, 48, 128)
# house_1 = pygame.Rect(112, height-896-96, 48, 128)
# house_2 = pygame.Rect(192, height-896-96, 48, 128)
# house_3 = pygame.Rect(272, height-896-96, 80, 128)

# road_0 = pygame.Rect(80, 608, 16, 16)
# road_1 = pygame.Rect(112, 608, 16, 16)
# road_x = pygame.Rect(48, 608, 16, 16)

# brick_0 = pygame.Rect(400, 784, 16, 16)
# brick_1 = pygame.Rect(432, 784, 16, 16)
# brick_2 = pygame.Rect(464, 784, 16, 16)
# brick_3 = pygame.Rect(400, 816, 16, 16)
# brick_4 = pygame.Rect(432, 816, 16, 16)
# brick_5 = pygame.Rect(464, 816, 16, 16)
# brick_6 = pygame.Rect(400, 848, 16, 16)
# brick_7 = pygame.Rect(432, 848, 16, 16)
# brick_8 = pygame.Rect(464, 848, 16, 16)

# 随机生成地图
residential_range = (10, 20)
shop_range = (5, 10)
k = 1  # 同方向道路的最小距离
city_map = generate_random_map(residential_range, shop_range, k)

# 将生成的地图绘制到屏幕上
def draw_map(screen, base_bg_image, city_map):
    for row in range(len(city_map)):
        for col in range(len(city_map[0])):
            if city_map[row][col] == 0:
                tmp = random.choice([brick_0, brick_1, brick_2, brick_3, brick_4, brick_5, brick_6, brick_7, brick_8])
                x, y = col * 16, row * 16
                screen.blit(base_bg_image, (x, y), tmp)
    
    for row in range(len(city_map)):
        for col in range(len(city_map[0])):
            if city_map[row][col] in {1, 2, -1}:
                if city_map[row][col] == 1:
                    tmp = road_0
                elif city_map[row][col] == 2:
                    tmp = road_1
                else:
                    tmp = road_x
                x, y = col * 16, row * 16
                screen.blit(base_bg_image, (x, y), tmp)

    for row in range(0, len(city_map), 2):
        for col in range(0, len(city_map[0]), 2):
            if city_map[row][col] in {3, 4}:
                if city_map[row][col] == 3:
                    tmp = random.choice([house_0, house_1, house_2, house_3])
                else:
                    tmp = random.choice([shop_0, shop_1, shop_2])
                x, y = col * 16, row * 16
                screen.blit(base_bg_image, (x, y), tmp)

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    draw_map(screen, base_bg_image, city_map)
    pygame.display.flip()

pygame.quit()
