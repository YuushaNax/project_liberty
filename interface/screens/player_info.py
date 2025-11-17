# interface/screens/player_info.py
import pygame as pg
from .base_screen import BaseScreen

FONT = pg.font.SysFont("consolas", 32)
TITLE = pg.font.SysFont("arial", 72)

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (10, 10, 10)

def draw_centered(surf, text, font, color, y):
    t = font.render(text, True, color)
    x = surf.get_width()//2 - t.get_width()//2
    surf.blit(t, (x, y))

class PlayerInfo(BaseScreen):
    def __init__(self, screen, data):
        super().__init__(screen)
        self.data = data

    def handle_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        draw_centered(self.screen, "📜 DATOS DEL PERSONAJE", TITLE, WHITE, 100)
        draw_centered(self.screen, f"Nombre: {self.data['name']}", FONT, WHITE, 300)
        draw_centered(self.screen, f"Raza: {list(self.data['race'].keys())[0]}", FONT, WHITE, 350)
        draw_centered(self.screen, f"Stats: {self.data['stats']}", FONT, WHITE, 400)
        draw_centered(self.screen, f"Edad: {self.data['age']}", FONT, WHITE, 450)
        draw_centered(self.screen, "ENTER para volver", FONT, GRAY, 600)
