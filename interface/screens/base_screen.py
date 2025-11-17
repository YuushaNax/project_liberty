# interface/screens/base_screen.py
import pygame as pg
import os

class BaseScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    # Loop propio de cada pantalla
    def run(self):
        clock = pg.time.Clock()
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    os._exit(0)
                self.handle_event(event)

            self.update()
            self.draw()
            pg.display.flip()
            clock.tick(30)
