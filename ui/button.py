import pygame

def draw_button(surface, text, x, y, width, height, color, hover_color,font,text_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
        pygame.draw.rect(surface, hover_color, (x, y, width, height))
    else:
        pygame.draw.rect(surface, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)

button_color = (200, 200, 200)
button_hover_color = (150, 150, 150)
button_x, button_y, button_width, button_height = 1280, 800, 400, 100
SHOW_MAIN_PAGE = 0
SHOW_SECOND_PAGE = 1
current_page = SHOW_MAIN_PAGE