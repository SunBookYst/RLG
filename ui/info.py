import pygame
import io
import sys
font = pygame.font.Font(None, 24)
text_color = (255, 255, 255)
bg_color = (0, 0, 0)
box_color = (50, 50, 50)
box_x, box_y, box_width, box_height = 1280, 0, 400, 800
console_output = io.StringIO()
sys.stdout = console_output

def render_text(text, font, color, bg_color):
    lines = text.splitlines()
    surfaces = [font.render(line, True, color, bg_color) for line in lines]
    return surfaces