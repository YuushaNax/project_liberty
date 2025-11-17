# interface/screens/text_input.py
import pygame as pg
from .base_screen import BaseScreen

FONT = pg.font.SysFont("consolas", 32)
WHITE = (255, 255, 255)
HIGHLIGHT = (100, 200, 255)
BLACK = (10, 10, 10)

def draw_centered(surface, text, font, color, y):
    s = font.render(text, True, color)
    x = surface.get_width()//2 - s.get_width()//2
    surface.blit(s, (x, y))

class TextInput(BaseScreen):
    def __init__(self, screen, prompt):
        super().__init__(screen)
        self.prompt = prompt
        self.text = ""
        self.result = None

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.result = self.text.strip()
                self.running = False
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self):
        self.screen.fill(BLACK)
        draw_centered(self.screen, self.prompt, FONT, WHITE, 300)
        draw_centered(self.screen, self.text + "_", FONT, HIGHLIGHT, 400)
