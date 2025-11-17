import pygame as pg
from screeninfo import get_monitors

def initialize_game():
    pg.init()  # 🔹 Inicializa pygame (input, sonido, etc.)

    for monitor in get_monitors():
        if monitor.is_primary:
            width, height = monitor.width, monitor.height

    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Project Liberty")

    # 🔹 Solo ahora importamos las pantallas (ya hay display y fuentes listas)
    from interface import screens as scr  

    menu = scr.main_menu.MainMenu(screen)
    choice = menu.run()

    if choice == "Salir":
        pg.quit()
        raise SystemExit
    elif choice == "Nueva Partida":
        print("→ Crear nueva partida")
        menu = scr.create_player.CreatePlayer(screen)
        menu.run()
    elif choice == "Cargar Partida":
        print("→ Cargar partida")
        menu = scr.load_player.LoadPlayer(screen)
        menu.run()
