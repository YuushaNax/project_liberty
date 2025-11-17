# interface/screens/create_player.py
import pygame as pg
import json
import random
import os
from pathlib import Path
from .base_screen import BaseScreen
from .text_input import TextInput
from engine.entities.entity import Entity

# === CONFIGURACIÓN DE INTERFAZ ===
# Nota: asumimos pg.init() y display ya inicializados antes de instanciar pantallas
FONT = pg.font.SysFont("consolas", 32)
TITLE = pg.font.SysFont("arial", 64)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
HIGHLIGHT = (100, 200, 255)
GREEN = (100, 255, 100)
BLACK = (10, 10, 10)

# === RUTAS BASE ===
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA = BASE_DIR / "data"
GAMES = BASE_DIR / "saves" / "games"


def draw_centered(surface, text, font, color, y):
    """Dibuja texto centrado horizontalmente."""
    s = font.render(str(text), True, color)
    x = surface.get_width() // 2 - s.get_width() // 2
    surface.blit(s, (x, y))


class CreatePlayer(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.phase = "name"

        # Cargar data desde JSON
        with open(DATA / "races.json", encoding="utf-8") as f:
            self.races = json.load(f)
        with open(DATA / "stats.json", encoding="utf-8") as f:
            self.stats_data = json.load(f)

        self.name = ""
        self.age = 0
        self.selected_race = None
        self.race_index = 0

    # -----------------------
    # Manejo de eventos (llamado por BaseScreen.run)
    # -----------------------
    def handle_event(self, event):
        # Para fases que no dependen de texto modal, aceptamos input directo
        if self.phase == "race":
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.race_index = (self.race_index - 1) % len(self.races)
                elif event.key == pg.K_DOWN:
                    self.race_index = (self.race_index + 1) % len(self.races)
                elif event.key in (pg.K_RETURN, pg.K_SPACE):
                    self.selected_race = self.races[self.race_index]
                    self.phase = "age"

        # En las demás fases no procesamos aquí porque usan TextInput modal o resumen
        elif self.phase == "finalize":
            # permitir cancelar con ESC si lo quieres (ejemplo)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False

    # ===============================
    # BUCLE PRINCIPAL DE ACTUALIZACIÓN
    # ===============================
    def update(self):
        # Las fases que necesitan texto usan TextInput (modal)
        if self.phase == "name":
            inp = TextInput(self.screen, "Nombre del personaje:")
            inp.run()
            # si el usuario canceló (entrada vacía), volvemos al menú
            if not inp.result:
                self.running = False
                return
            self.name = inp.result
            self.phase = "race"

        elif self.phase == "race":
            # aquí solo hacemos lógica por frame si hace falta (por ahora nada)
            pass

        elif self.phase == "age":
            inp = TextInput(self.screen, "Edad del personaje (ej: 18):",)
            inp.run()
            if not inp.result:
                # cancelar si desea
                self.running = False
                return
            try:
                self.age = int(inp.result)
                self.phase = "finalize"
            except ValueError:
                # si es inválido, regresar a la fase age para reingresar
                self.age = 0
                self.phase = "age"

        elif self.phase == "finalize":
            self.save_player()
            self.show_summary()
            self.running = False

    # ===============================
    # DIBUJADO POR FASE
    # ===============================
    def draw(self):
        self.screen.fill(BLACK)

        if self.phase == "race":
            draw_centered(self.screen, "Selecciona tu raza:", TITLE, WHITE, 150)
            # dibujar un máximo de N items en pantalla si hay muchas razas
            for i, race in enumerate(self.races):
                color = HIGHLIGHT if i == self.race_index else GRAY
                draw_centered(self.screen, race.get("display", f"race_{i}"), FONT, color, 300 + i * 60)

        elif self.phase == "finalize":
            draw_centered(self.screen, "Creando personaje...", FONT, WHITE, 400)

        # Nota: BaseScreen.run hará pg.display.flip() y tick

    # ===============================
    # GUARDADO Y RESUMEN
    # ===============================
    def save_player(self):
        stats = {s["stat_name"]: 10 for s in self.stats_data}
        for mod in self.selected_race.get("modifiers", []):
            if mod["stat_name"] in stats:
                stats[mod["stat_name"]] += mod["modifier"]

        player = Entity(
            name=self.name,
            new_stats=stats,
            height=random.randint(
                int(self.selected_race.get("min_height", 150)),
                int(self.selected_race.get("max_height", 190)),
            ),
        )
        player.race = {self.selected_race.get("race_name", self.selected_race.get("display")): 100}
        player.age = self.age

        os.makedirs(GAMES, exist_ok=True)
        path = GAMES / f"{self.name.lower().replace(' ', '_')}.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "name": player.name,
                    "race": player.race,
                    "age": player.age,
                    "stats": player.stats,
                    "height": player.height,
                },
                f,
                indent=4,
            )

    def show_summary(self):
        waiting = True
        while waiting:
            self.screen.fill(BLACK)
            draw_centered(self.screen, "✅ PERSONAJE CREADO", TITLE, GREEN, 100)
            draw_centered(self.screen, f"Nombre: {self.name}", FONT, WHITE, 300)
            draw_centered(
                self.screen, f"Raza: {self.selected_race.get('display','?')}", FONT, WHITE, 350
            )
            draw_centered(self.screen, f"Edad: {self.age}", FONT, WHITE, 400)
            draw_centered(self.screen, "Presiona ENTER para continuar", FONT, GRAY, 600)

            pg.display.flip()
            self.clock.tick(30)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    waiting = False
