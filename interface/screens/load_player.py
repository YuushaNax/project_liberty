# interface/screens/load_player.py
import pygame as pg
import json
from pathlib import Path
from .base_screen import BaseScreen
from .exploration import Exploration
from engine.world.world import World

FONT = pg.font.SysFont("consolas", 32)
TITLE_FONT = pg.font.SysFont("arial", 64)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
HIGHLIGHT = (100, 200, 255)
BLACK = (10, 10, 10)
RED = (255, 100, 100)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
GAMES = BASE_DIR / "saves" / "games"

def draw_centered(surface, text, font, color, y):
    s = font.render(text, True, color)
    x = surface.get_width() // 2 - s.get_width() // 2
    surface.blit(s, (x, y))

def draw_text(surface, text, font, color, x, y):
    s = font.render(text, True, color)
    surface.blit(s, (x, y))

class LoadPlayer(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.sessions = World.get_session_list()
        self.index = 0
        self.message = ""
        self.message_time = 0
        self.clock = pg.time.Clock()

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.running = False
            
            elif event.key == pg.K_UP:
                if self.sessions:
                    self.index = (self.index - 1) % len(self.sessions)
            
            elif event.key == pg.K_DOWN:
                if self.sessions:
                    self.index = (self.index + 1) % len(self.sessions)
            
            elif event.key in (pg.K_RETURN, pg.K_SPACE):
                if self.sessions:
                    self.load_session(self.sessions[self.index])
            
            elif event.key == pg.K_DELETE:
                # Eliminar sesión
                if self.sessions:
                    self.delete_session(self.sessions[self.index])

    def load_session(self, session_name):
        """Carga una sesión guardada."""
        try:
            world = World(session_name=session_name)
            if world.load_game():
                # Pasar a exploración
                exploration_screen = Exploration(
                    self.screen,
                    player_data=world.player_data,
                    world_seed=world.seed,
                    session_name=session_name
                )
                exploration_screen.run()
                self.running = False
            else:
                self.message = "Error al cargar la partida"
                self.message_time = 120
        except Exception as e:
            self.message = f"Error: {str(e)[:40]}"
            self.message_time = 120

    def delete_session(self, session_name):
        """Elimina una sesión guardada."""
        try:
            session_dir = GAMES / session_name
            save_file = session_dir / "save.json"
            
            if save_file.exists():
                save_file.unlink()
                self.message = f"Sesion '{session_name}' eliminada"
                self.message_time = 120
                self.sessions = World.get_session_list()
                if self.index >= len(self.sessions) and self.sessions:
                    self.index = len(self.sessions) - 1
        except Exception as e:
            self.message = f"Error al eliminar: {str(e)[:40]}"
            self.message_time = 120

    def update(self):
        """Actualiza la lógica."""
        if self.message_time > 0:
            self.message_time -= 1

    def draw(self):
        self.screen.fill(BLACK)
        
        # Título
        draw_centered(self.screen, "CARGAR PARTIDA", TITLE_FONT, WHITE, 50)
        
        # Instrucciones
        draw_centered(self.screen, "Selecciona una sesion guardada", FONT, GRAY, 150)
        draw_text(self.screen, "[ARRIBA/ABAJO] Navegar  [ENTER] Cargar  [DEL] Eliminar  [ESC] Volver", 
                 FONT, GRAY, 20, self.screen.get_height() - 60)
        
        if not self.sessions:
            draw_centered(self.screen, "No hay partidas guardadas", FONT, RED, 300)
        else:
            # Mostrar sesiones
            start_y = 250
            for i, session_name in enumerate(self.sessions):
                color = HIGHLIGHT if i == self.index else GRAY
                
                # Nombre de la sesión
                draw_centered(self.screen, f"> {session_name} <", FONT, color, start_y + i * 70)
                
                # Información de la sesión
                try:
                    session_dir = GAMES / session_name
                    save_file = session_dir / "save.json"
                    
                    if save_file.exists():
                        with open(save_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            player_name = data.get("player", {}).get("name", "Desconocido")
                            pos = data.get("world", {}).get("player_position", {})
                            x, y = pos.get("x", 0), pos.get("y", 0)
                            info = f"  Posicion: ({x}, {y})"
                            draw_text(self.screen, info, FONT, GRAY, 100, start_y + i * 70 + 35)
                except:
                    pass
        
        # Mensaje
        if self.message_time > 0:
            draw_centered(self.screen, self.message, FONT, HIGHLIGHT, 150)
