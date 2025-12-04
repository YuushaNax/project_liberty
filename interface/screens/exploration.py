# interface/screens/exploration.py
"""
Pantalla de exploración del mundo.
Permite al jugador navegar por el mapa, ver información de terrenos y gestionar su viaje.
"""

import pygame as pg
from pathlib import Path
from .base_screen import BaseScreen
from engine.world.world import World

# === CONFIGURACIÓN DE INTERFAZ ===
FONT_SMALL = pg.font.SysFont("consolas", 18)
FONT_NORMAL = pg.font.SysFont("consolas", 24)
FONT_TITLE = pg.font.SysFont("arial", 48)
FONT_SUBTITLE = pg.font.SysFont("arial", 32)

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
HIGHLIGHT = (100, 200, 255)
GOLD = (255, 215, 0)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
BLACK = (10, 10, 10)

TILE_SIZE = 12  # Pixels por celda en la visualización
LEGEND_WIDTH = 250


def draw_text(surface, text, font, color, x, y):
    """Dibuja texto en posición específica."""
    s = font.render(str(text), True, color)
    surface.blit(s, (x, y))


def draw_centered(surface, text, font, color, y, x=None):
    """Dibuja texto centrado horizontalmente."""
    s = font.render(str(text), True, color)
    if x is None:
        x = surface.get_width() // 2 - s.get_width() // 2
    surface.blit(s, (x, y))


class Exploration(BaseScreen):
    """Pantalla de exploración del mundo."""
    
    def __init__(self, screen, player_data=None, world_seed=42, session_name="default"):
        """
        Inicializa la pantalla de exploración.
        
        Args:
            screen: Superficie pygame de pantalla
            player_data: Datos del jugador creado
            world_seed: Semilla para generación del mundo
            session_name: Nombre de la sesión para guardado
        """
        super().__init__(screen)
        self.player_data = player_data or {}
        self.session_name = session_name
        self.world = World(seed=world_seed, session_name=session_name)
        
        # Generar mundo
        self.world.generate_world(width=128, height=128)
        self.world.player_data = self.player_data  # Asignar datos del jugador
        self.world.load_local_map()
        
        # Estado de la interfaz
        self.show_legend = False
        self.show_local_map = False  # Nuevo: mostrar mapa local detallado
        self.message = "¡Bienvenido a tu nuevo mundo!"
        self.message_time = 0
        self.clock = pg.time.Clock()
        
        # Centro de vista del mapa en pantalla
        self.view_center_x = self.screen.get_width() // 2
        self.view_center_y = self.screen.get_height() // 2 - 100
        
        # Contador para guardado automático (cada 30 segundos)
        self.autosave_counter = 0
        self.autosave_interval = 1800  # 30 segundos a 60 FPS
    
    def handle_event(self, event):
        """Maneja eventos de entrada."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                # Guardar antes de salir
                self.world.save_game()
                self.running = False
            
            elif event.key == pg.K_UP or event.key == pg.K_w:
                if self.world.move_player("up"):
                    self.message = "Moviste hacia arriba."
                else:
                    self.message = "No puedes ir hacia arriba."
                self.message_time = 60
            
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                if self.world.move_player("down"):
                    self.message = "Moviste hacia abajo."
                else:
                    self.message = "No puedes ir hacia abajo."
                self.message_time = 60
            
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                if self.world.move_player("left"):
                    self.message = "Moviste hacia la izquierda."
                else:
                    self.message = "No puedes ir hacia la izquierda."
                self.message_time = 60
            
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                if self.world.move_player("right"):
                    self.message = "Moviste hacia la derecha."
                else:
                    self.message = "No puedes ir hacia la derecha."
                self.message_time = 60
            
            elif event.key == pg.K_l:
                # Toggle leyenda
                self.show_legend = not self.show_legend
                self.show_local_map = False  # Desactivar mapa local al ver leyenda
            
            elif event.key == pg.K_m:
                # Toggle mapa local detallado (NUEVO)
                self.show_local_map = not self.show_local_map
                self.show_legend = False  # Desactivar leyenda al ver mapa local
                if self.show_local_map:
                    self.message = "Mapa Local Detallado (64x64 - Zoom)"
                    self.message_time = 120
            
            elif event.key == pg.K_i:
                # Mostrar información detallada
                terrain_info = self.world.get_current_terrain_info()
                if terrain_info:
                    self.message = f"{terrain_info['terrain_name']} - Temp: {terrain_info['temperature_category']}"
                    self.message_time = 180
            
            elif event.key == pg.K_F5:
                # Guardar manualmente
                self.world.save_game()
                self.message = f"Partida guardada - Sesion: {self.session_name}"
                self.message_time = 120
    
    def update(self):
        """Actualiza la lógica del juego."""
        if self.message_time > 0:
            self.message_time -= 1
        else:
            self.message = ""
        
        # Guardado automático
        self.autosave_counter += 1
        if self.autosave_counter >= self.autosave_interval:
            self.world.save_game()
            self.autosave_counter = 0
    
    def draw(self):
        """Dibuja la pantalla."""
        self.screen.fill(BLACK)
        
        # Título
        draw_centered(self.screen, "EXPLORACIÓN DEL MUNDO", FONT_TITLE, WHITE, 20)
        
        # Información del jugador
        player_name = self.player_data.get("name", "Aventurero")
        player_race = list(self.player_data.get("race", {}).keys())[0] if self.player_data.get("race") else "Desconocido"
        draw_text(self.screen, f"Personaje: {player_name} ({player_race})", FONT_NORMAL, GOLD, 20, 70)
        
        # Información de posición y terreno
        terrain_info = self.world.get_current_terrain_info()
        if terrain_info:
            pos = terrain_info["position"]
            terrain_name = terrain_info["terrain_name"]
            temp = terrain_info["temperature_category"]
            draw_text(self.screen, f"Posición: ({pos[0]}, {pos[1]}) | Terreno: {terrain_name} | Temp: {temp}", 
                     FONT_NORMAL, GRAY, 20, 110)
        
        # Mostrar estado actual (Global vs Local)
        if self.show_local_map:
            status_text = ">>> VISTA LOCAL DETALLADA (M para volver) <<<"
            status_color = (100, 255, 100)
        else:
            status_text = ">>> VISTA GLOBAL (M para zoom local) <<<"
            status_color = (100, 200, 255)
        
        draw_centered(self.screen, status_text, FONT_NORMAL, status_color, 130)
        
        # MOSTRAR MAPA LOCAL DETALLADO
        if self.show_local_map:
            self.draw_local_map()
        else:
            # Mostrar mapa mundial (comportamiento original)
            map_area_width = self.screen.get_width() - LEGEND_WIDTH if self.show_legend else self.screen.get_width()
            map_area_height = self.screen.get_height() - 150
            self.draw_world_map(map_area_width, map_area_height)
            
            # Leyenda si está activada
            if self.show_legend:
                self.draw_legend()
        
        # Área de información inferior
        if not self.show_local_map:  # Solo mostrar info panel en vista global
            self.draw_info_panel()
        
        # Controles dinámicos según vista
        controls = []
        if self.show_local_map:
            controls = [
                "WASD/FLECHAS: Mover | M: Volver a Vista Global | I: Info Terreno | ESC: Salir"
            ]
        else:
            controls = [
                "WASD/FLECHAS: Mover | L: Leyenda | M: Zoom Local | I: Info | ESC: Salir | F5: Guardar"
            ]
        
        y = self.screen.get_height() - 40
        for control in controls:
            draw_centered(self.screen, control, FONT_SMALL, DARK_GRAY, y)
            y += 25
        # Mensaje
        if self.message:
            msg_y = self.screen.get_height() - 100
            draw_centered(self.screen, self.message, FONT_NORMAL, HIGHLIGHT, msg_y)
    
    def draw_world_map(self, map_width, map_height):
        """
        Dibuja el mapa del mundo con el jugador en el centro.
        Similar a Battle Brothers - vista estratégica global.
        
        Args:
            map_width: Ancho del área del mapa
            map_height: Alto del área del mapa
        """
        map_x = 20
        map_y = 150
        
        # Dibujar fondo del mapa
        pg.draw.rect(self.screen, (20, 20, 30), (map_x, map_y, map_width - 40, map_height - 30))
        pg.draw.rect(self.screen, HIGHLIGHT, (map_x, map_y, map_width - 40, map_height - 30), 2)
        
        if self.world.world_map is None:
            return
        
        world_height, world_width = self.world.world_map.shape
        
        # Calcular ventana visible (siempre muestra jugador en centro)
        view_tiles_x = (map_width - 40) // TILE_SIZE
        view_tiles_y = (map_height - 30) // TILE_SIZE
        
        view_start_x = max(0, self.world.player_world_x - view_tiles_x // 2)
        view_start_y = max(0, self.world.player_world_y - view_tiles_y // 2)
        
        view_end_x = min(world_width, view_start_x + view_tiles_x)
        view_end_y = min(world_height, view_start_y + view_tiles_y)
        
        # Dibujar tiles
        for y in range(view_start_y, view_end_y):
            for x in range(view_start_x, view_end_x):
                tile = self.world.world_map[y, x]
                color = tile.get_color()
                
                screen_x = map_x + 20 + (x - view_start_x) * TILE_SIZE
                screen_y = map_y + 15 + (y - view_start_y) * TILE_SIZE
                
                pg.draw.rect(self.screen, color, (screen_x, screen_y, TILE_SIZE - 1, TILE_SIZE - 1))
        
        # Dibujar región actual como rectángulo de referencia
        region_x = self.world.player_world_x // 64
        region_y = self.world.player_world_y // 64
        region_start_x = region_x * 64
        region_start_y = region_y * 64
        region_end_x = min(world_width, region_start_x + 64)
        region_end_y = min(world_height, region_start_y + 64)
        
        # Solo dibujar si la región está visible
        if view_start_x < region_end_x and view_end_x > region_start_x and \
           view_start_y < region_end_y and view_end_y > region_start_y:
            rect_start_x = map_x + 20 + max(0, region_start_x - view_start_x) * TILE_SIZE
            rect_start_y = map_y + 15 + max(0, region_start_y - view_start_y) * TILE_SIZE
            rect_width = (min(region_end_x, view_end_x) - max(region_start_x, view_start_x)) * TILE_SIZE
            rect_height = (min(region_end_y, view_end_y) - max(region_start_y, view_start_y)) * TILE_SIZE
            
            pg.draw.rect(self.screen, (100, 200, 100), (rect_start_x, rect_start_y, rect_width, rect_height), 2)
        
        # Dibujar indicador del jugador (más prominente)
        player_screen_x = map_x + 20 + (self.world.player_world_x - view_start_x) * TILE_SIZE
        player_screen_y = map_y + 15 + (self.world.player_world_y - view_start_y) * TILE_SIZE
        pg.draw.rect(self.screen, GOLD, (player_screen_x, player_screen_y, TILE_SIZE - 1, TILE_SIZE - 1), 3)
        pg.draw.circle(self.screen, GOLD, 
                      (player_screen_x + TILE_SIZE // 2, player_screen_y + TILE_SIZE // 2), 5)
        
        # Mostrar información de posición
        draw_text(self.screen, f"MAPA GLOBAL (128x128) - Posicion: ({self.world.player_world_x}, {self.world.player_world_y})", 
                 FONT_NORMAL, HIGHLIGHT, map_x, map_y - 30)
        draw_text(self.screen, f"Region detectada: ({region_x}, {region_y}) [Presiona M para zoom]", 
                 FONT_SMALL, GRAY, map_x, map_y - 5)
    
    def draw_legend(self):
        """Dibuja la leyenda de terrenos."""
        legend_x = self.screen.get_width() - LEGEND_WIDTH - 10
        legend_y = 150
        
        # Fondo de leyenda
        pg.draw.rect(self.screen, (30, 30, 40), (legend_x, legend_y, LEGEND_WIDTH, 400))
        pg.draw.rect(self.screen, GRAY, (legend_x, legend_y, LEGEND_WIDTH, 400), 2)
        
        # Título
        draw_text(self.screen, "LEYENDA", FONT_SUBTITLE, WHITE, legend_x + 10, legend_y + 10)
        
        # Terrenos
        legend_items = [
            ("~", "Océano", (20, 80, 150)),
            (".", "Agua Poco Prof.", (100, 150, 200)),
            ("s", "Arena", (210, 180, 80)),
            ("g", "Hierba", (100, 180, 80)),
            ("f", "Bosque", (60, 120, 40)),
            ("^", "Montaña", (140, 100, 60)),
            ("A", "Picos Nevados", (240, 240, 255)),
            ("@", "Arena Combate", (200, 140, 40)),
            ("#", "Grieta", (40, 20, 30)),
        ]
        
        y_offset = legend_y + 50
        for symbol, name, color in legend_items:
            # Dibujar color
            pg.draw.rect(self.screen, color, (legend_x + 10, y_offset, 20, 20))
            # Dibujar nombre
            draw_text(self.screen, f"{name}", FONT_SMALL, GRAY, legend_x + 40, y_offset + 2)
            y_offset += 25
    
    def draw_info_panel(self):
        """Dibuja el panel de información inferior."""
        panel_y = self.screen.get_height() - 140
        
        # Fondo del panel
        pg.draw.rect(self.screen, (30, 30, 40), (20, panel_y, self.screen.get_width() - 40, 130))
        pg.draw.rect(self.screen, GRAY, (20, panel_y, self.screen.get_width() - 40, 130), 2)
        
        # Título
        draw_text(self.screen, "INFORMACIÓN DE POSICIÓN", FONT_NORMAL, WHITE, 30, panel_y + 10)
        
        # Información del terreno actual
        terrain_info = self.world.get_current_terrain_info()
        nearby_info = self.world.get_nearby_terrain_info(radius=1)
        
        if terrain_info:
            y = panel_y + 40
            draw_text(self.screen, f"Terreno: {terrain_info['terrain_name']}", FONT_NORMAL, HIGHLIGHT, 30, y)
            draw_text(self.screen, f"Temperatura: {terrain_info['temperature_category']}", FONT_NORMAL, GRAY, 30, y + 25)
            draw_text(self.screen, f"Altura: {terrain_info['height']:.2f}", FONT_NORMAL, GRAY, 400, y)
            draw_text(self.screen, f"Temp: {terrain_info['temperature']:.2f}", FONT_NORMAL, GRAY, 400, y + 25)
            
            # Terrenos cercanos caminables
            walkable = [name for name, info in nearby_info.items() if info["walkable"]]
            if walkable:
                directions = ", ".join(walkable[:4])
                draw_text(self.screen, f"Puedes ir a: {directions}", FONT_SMALL, GREEN, 700, y)
            
            # Terrenos cercanos no caminables
            non_walkable = [name for name, info in nearby_info.items() if not info["walkable"]]
            if non_walkable:
                blocked = ", ".join(non_walkable[:4])
                draw_text(self.screen, f"Bloqueado por: {blocked}", FONT_SMALL, RED, 700, y + 25)
    
    def draw_local_map(self):
        """Dibuja el mapa local detallado (64x64) similar a Battle Brothers."""
        if self.world.current_local_map is None:
            self.world.load_local_map()
            if self.world.current_local_map is None:
                return
        
        map_x = 20
        map_y = 150
        local_width = self.screen.get_width() - 40
        local_height = self.screen.get_height() - 200
        
        # Dibujar fondo del mapa
        pg.draw.rect(self.screen, (20, 20, 30), (map_x, map_y, local_width, local_height))
        pg.draw.rect(self.screen, HIGHLIGHT, (map_x, map_y, local_width, local_height), 3)
        
        # Tamaño de cada tile local
        tile_size_x = max(2, local_width // 64)
        tile_size_y = max(2, local_height // 64)
        
        # Dibujar tiles del mapa local
        local_map = self.world.current_local_map
        for y in range(64):
            for x in range(64):
                tile = local_map[y, x]
                color = tile.get_color()
                
                screen_x = map_x + x * tile_size_x
                screen_y = map_y + y * tile_size_y
                
                pg.draw.rect(self.screen, color, (screen_x, screen_y, tile_size_x - 1, tile_size_y - 1))
        
        # Calcular posición del jugador dentro del mapa local (64x64)
        player_local_x = self.world.player_world_x % 64
        player_local_y = self.world.player_world_y % 64
        
        # Dibujar indicador del jugador
        player_screen_x = map_x + player_local_x * tile_size_x
        player_screen_y = map_y + player_local_y * tile_size_y
        pg.draw.rect(self.screen, GOLD, (player_screen_x, player_screen_y, tile_size_x - 1, tile_size_y - 1), 2)
        pg.draw.circle(self.screen, GOLD, 
                      (player_screen_x + tile_size_x // 2, player_screen_y + tile_size_y // 2), 3)
        
        # Dibujar información
        region_x = self.world.player_world_x // 64
        region_y = self.world.player_world_y // 64
        
        info_y = map_y + local_height + 10
        draw_text(self.screen, f"MAPA LOCAL DETALLADO - Region: ({region_x}, {region_y})", 
                 FONT_NORMAL, HIGHLIGHT, map_x, info_y)
        draw_text(self.screen, f"Posicion Global: ({self.world.player_world_x}, {self.world.player_world_y}) | Local: ({player_local_x}, {player_local_y})", 
                 FONT_SMALL, GRAY, map_x, info_y + 30)
        
        # Mostrar terreno actual
        terrain_info = self.world.get_current_terrain_info()
        if terrain_info:
            draw_text(self.screen, f"Terreno: {terrain_info['terrain_name']}", 
                     FONT_NORMAL, GREEN, map_x, info_y + 60)
