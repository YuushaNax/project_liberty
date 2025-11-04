import os
import pygame as pg
from screeninfo import get_monitors


def initialize_game():
    global monitor_height, monitor_width
    for monitor in get_monitors():
        if monitor.is_primary:
            monitor_height = monitor.height
            monitor_width = monitor.width

    pg.init()
    screen = pg.display.set_mode((monitor_width, monitor_height))
    pg.display.set_caption("Mi Juego")
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                os._exit(0)

