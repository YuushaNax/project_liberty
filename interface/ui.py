import os
import pygame as pg
import json
import random
from screeninfo import get_monitors
from pathlib import Path
from saves.utilities.entity import Entity

# === CONFIGURACIÓN GENERAL ===
pg.init()
pg.font.init()

FONT = pg.font.SysFont("consolas", 32)
TITLE_FONT = pg.font.SysFont("arial", 72)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
HIGHLIGHT = (100, 200, 255)
BLACK = (10, 10, 10)
GREEN = (100, 255, 100)

# === RUTAS PORTABLES ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
GAMES_DIR = BASE_DIR / "saves" / "games"
RACES_PATH = DATA_DIR / "races.json"
STATS_PATH = DATA_DIR / "stats.json"


# =============================
# FUNCIONES AUXILIARES DE TEXTO
# =============================
def draw_centered_text(surface, text, font, color, y):
    text_surface = font.render(text, True, color)
    x = surface.get_width() // 2 - text_surface.get_width() // 2
    surface.blit(text_surface, (x, y))


# =============================
# MENÚ PRINCIPAL
# =============================
def show_menu(screen):
    clock = pg.time.Clock()
    options = ["Nueva Partida", "Cargar Partida", "Salir"]
    selected = 0

    while True:
        screen.fill(BLACK)
        draw_centered_text(screen, "PROJECT LIBERTY", TITLE_FONT, WHITE, 150)

        for i, opt in enumerate(options):
            color = HIGHLIGHT if i == selected else GRAY
            draw_centered_text(screen, opt, FONT, color, 350 + i * 80)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                os._exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pg.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key in (pg.K_RETURN, pg.K_SPACE):
                    return options[selected]
        clock.tick(30)


# =============================
# ENTRADA DE TEXTO
# =============================
def text_input(screen, prompt):
    clock = pg.time.Clock()
    user_text = ""
    while True:
        screen.fill(BLACK)
        draw_centered_text(screen, prompt, FONT, WHITE, 300)
        draw_centered_text(screen, user_text + "_", FONT, HIGHLIGHT, 400)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                os._exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return user_text.strip()
                elif event.key == pg.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
        clock.tick(30)


# =============================
# CREAR NUEVO PERSONAJE
# =============================
def create_new_player(screen):
    # Cargar data
    with open(RACES_PATH, "r", encoding="utf-8") as f:
        races = json.load(f)
    with open(STATS_PATH, "r", encoding="utf-8") as f:
        stats_data = json.load(f)

    # Nombre
    name = text_input(screen, "Nombre del personaje:")

    # Selección de raza
    clock = pg.time.Clock()
    index = 0
    while True:
        screen.fill(BLACK)
        draw_centered_text(screen, "Selecciona tu raza:", FONT, WHITE, 200)
        for i, race in enumerate(races):
            color = HIGHLIGHT if i == index else GRAY
            draw_centered_text(screen, race["display"], FONT, color, 300 + i * 60)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                os._exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    index = (index - 1) % len(races)
                elif event.key == pg.K_DOWN:
                    index = (index + 1) % len(races)
                elif event.key in (pg.K_RETURN, pg.K_SPACE):
                    selected_race = races[index]
                    break
        else:
            clock.tick(30)
            continue
        break

    # Edad
    while True:
        age_input = text_input(screen, "Edad del personaje (ej: 18):")
        if age_input.isdigit() and int(age_input) > 0:
            age = int(age_input)
            break

    # Stats base
    stats = {s["stat_name"]: 10 for s in stats_data}
    for mod in selected_race["modifiers"]:
        if mod["stat_name"] in stats:
            stats[mod["stat_name"]] += mod["modifier"]

    # Crear jugador
    player = Entity(name=name, new_stats=stats, height=random.randint(int(selected_race["min_height"]), int(selected_race["max_height"])))
    player.race = {selected_race["race_name"]: 100}
    player.age = age

    # Guardar
    os.makedirs(GAMES_DIR, exist_ok=True)
    save_path = GAMES_DIR / f"{name.lower().replace(' ', '_')}.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": player.name,
            "race": player.race,
            "age": player.age,
            "stats": player.stats,
            "height": player.height
        }, f, indent=4)

    # Mostrar resumen
    while True:
        screen.fill(BLACK)
        draw_centered_text(screen, "✅ PERSONAJE CREADO", TITLE_FONT, GREEN, 100)
        draw_centered_text(screen, f"Nombre: {player.name}", FONT, WHITE, 300)
        draw_centered_text(screen, f"Raza: {list(player.race.keys())[0]}", FONT, WHITE, 350)
        draw_centered_text(screen, f"Estadísticas: {player.stats}", FONT, WHITE, 400)
        draw_centered_text(screen, f"Edad: {player.age}", FONT, WHITE, 400)
        draw_centered_text(screen, "Presiona ENTER para volver al menú", FONT, GRAY, 600)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                return


# =============================
# CARGAR PERSONAJE GUARDADO
# =============================
def load_player(screen):
    files = [f for f in os.listdir(GAMES_DIR) if f.endswith(".json")]
    if not files:
        while True:
            screen.fill(BLACK)
            draw_centered_text(screen, "⚠️ No hay partidas guardadas", FONT, WHITE, 400)
            draw_centered_text(screen, "Presiona ENTER para volver", FONT, GRAY, 500)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    return

    index = 0
    clock = pg.time.Clock()
    while True:
        screen.fill(BLACK)
        draw_centered_text(screen, "Selecciona una partida:", FONT, WHITE, 200)
        for i, f in enumerate(files):
            color = HIGHLIGHT if i == index else GRAY
            draw_centered_text(screen, f, FONT, color, 300 + i * 60)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                os._exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    index = (index - 1) % len(files)
                elif event.key == pg.K_DOWN:
                    index = (index + 1) % len(files)
                elif event.key in (pg.K_RETURN, pg.K_SPACE):
                    with open(GAMES_DIR / files[index], "r", encoding="utf-8") as f:
                        data = json.load(f)
                    show_player_info(screen, data)
                    return
        clock.tick(30)


def show_player_info(screen, data):
    while True:
        screen.fill(BLACK)
        draw_centered_text(screen, "📜 DATOS DEL PERSONAJE", TITLE_FONT, WHITE, 100)
        draw_centered_text(screen, f"Nombre: {data['name']}", FONT, WHITE, 300)
        draw_centered_text(screen, f"Raza: {list(data['race'].keys())[0]}", FONT, WHITE, 350)
        draw_centered_text(screen, f"Estadísticas: {data['stats']}", FONT, WHITE, 400)
        draw_centered_text(screen, f"Edad: {data['age']}", FONT, WHITE, 400)
        draw_centered_text(screen, "Presiona ENTER para volver", FONT, GRAY, 600)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                return


# =============================
# LOOP PRINCIPAL
# =============================
def initialize_game():
    for monitor in get_monitors():
        if monitor.is_primary:
            width, height = monitor.width, monitor.height

    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Project Liberty")

    while True:
        choice = show_menu(screen)
        if choice == "Nueva Partida":
            create_new_player(screen)
        elif choice == "Cargar Partida":
            load_player(screen)
        elif choice == "Salir":
            pg.quit()
            os._exit(0)
