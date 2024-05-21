import pygame
import io
import sys
font_path = "C:\Windows\Fonts\simhei.ttf"
font = pygame.font.Font(font_path, 20)
text_color = (255, 255, 255)
bg_color = (50, 50, 50)
box_color = (50, 50, 50)
fixed_text_color = (0, 255, 0)
variable_text_color = (192, 192, 192)
box_x, box_y, box_width, box_height = 1280, 0, 400, 800
console_output = io.StringIO()
sys.stdout = console_output

life = 100
assets = 5000
supplies = 300

def render_status(surface):
    surface.fill(box_color)
    fixed_text = "生命值: "
    variable_text = str(life)
    text_surf = font.render(fixed_text, True, fixed_text_color)
    surface.blit(text_surf, (5, 5))
    text_surf = font.render(variable_text, True, variable_text_color)
    surface.blit(text_surf, (35 + text_surf.get_width() + 10, 5))

    fixed_text = "资产: "
    variable_text = str(assets)
    text_surf = font.render(fixed_text, True, fixed_text_color)
    surface.blit(text_surf, (5, 35))
    text_surf = font.render(variable_text, True, variable_text_color)
    surface.blit(text_surf, (15 + text_surf.get_width() + 10, 35))

    fixed_text = "物资: "
    variable_text = str(supplies)
    text_surf = font.render(fixed_text, True, fixed_text_color)
    surface.blit(text_surf, (5, 65))
    text_surf = font.render(variable_text, True, variable_text_color)
    surface.blit(text_surf, (20 + text_surf.get_width() + 10, 65))


def render_text(text):
    lines = text.splitlines()
    surfaces = [font.render(line, True, text_color, bg_color) for line in lines]
    return surfaces