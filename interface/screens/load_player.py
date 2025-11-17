# interface/screens/load_player.py
import pygame as pg
import os
import json
from pathlib import Path
from .base_screen import BaseScreen
from .player_info import PlayerInfo

FONT = pg.font.SysFont("consolas", 32)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
HIGHLIGHT = (100, 200, 255)
BLACK = (10, 10, 10)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
GAMES = BASE_DIR/"saves"/"games"

def draw_centered(surface, text, font, color, y):
    s = font.render(text, True, color)
    x = surface.get_width()//2 - s.get_width()//2
    surface.blit(s, (x, y))

class LoadPlayer(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.files = [f for f in os.listdir(GAMES) if f.endswith(".json")]
        self.index = 0

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.index = (self.index - 1) % len(self.files)
            elif event.key == pg.K_DOWN:
                self.index = (self.index + 1) % len(self.files)
            elif event.key in (pg.K_RETURN, pg.K_SPACE):
                with open(GAMES/self.files[self.index], encoding="utf-8") as f:
                    data = json.load(f)

                info = PlayerInfo(self.screen, data)
                info.run()
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        draw_centered(self.screen, "Selecciona una partida:", FONT, WHITE, 200)

        for i, file in enumerate(self.files):
            color = HIGHLIGHT if i == self.index else GRAY
            draw_centered(self.screen, file, FONT, color, 300 + i*60)
