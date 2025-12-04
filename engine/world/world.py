# engine/world/world.py
"""
Sistema de gestión del mundo del juego.
Maneja el estado global, posición del jugador, mapa generado y navegación.
"""

import json
from pathlib import Path
from engine.world.map_generator import MapGenerator, Terrain
import numpy as np


class World:
    """Gestor principal del mundo."""
    
    def __init__(self, seed=42, session_name="default"):
        """
        Inicializa el mundo.
        
        Args:
            seed: Semilla para generación procedural
            session_name: Nombre de la sesión para guardado
        """
        self.seed = seed
        self.session_name = session_name
        self.generator = MapGenerator(seed=seed, world_size=128)  # Mundo más grande
        
        # Posición del jugador en el mapa mundial (será actualizada en generate_world)
        self.player_world_x = 0
        self.player_world_y = 0
        
        # Mapa mundial generado
        self.world_map = None
        self.current_local_map = None
        
        # Cache para el mapa local: (región_x, región_y) -> mapa_local
        # Cada región es de 64x64, así que almacenaremos 4 regiones cercanas
        self.local_map_cache = {}
        self.cached_region_x = None
        self.cached_region_y = None
        
        # Datos del jugador
        self.player_data = None
    
    def generate_world(self, width=128, height=128):
        """
        Genera el mapa mundial.
        
        Args:
            width: Ancho del mapa
            height: Alto del mapa
        
        Returns:
            Array 2D de MapTile
        """
        self.world_map = self.generator.generate_world_map(width=width, height=height)
        
        # Establecer posición inicial del jugador en un lugar caminable
        # Optimizado: buscar solo en el centro del mapa
        center_x, center_y = width // 2, height // 2
        search_radius = min(width, height) // 4
        
        # Primera pasada: buscar en área cercana al centro
        for distance in range(0, search_radius):
            found = False
            for dy in range(-distance, distance + 1):
                for dx in range(-distance, distance + 1):
                    if abs(dx) < distance and abs(dy) < distance:
                        continue  # Solo buscar en los bordes del cuadrado
                    
                    x = center_x + dx
                    y = center_y + dy
                    
                    if 0 <= x < width and 0 <= y < height:
                        if self.is_terrain_walkable(self.world_map[y, x].terrain):
                            self.player_world_x = x
                            self.player_world_y = y
                            return self.world_map
        
        # Fallback: encontrar cualquier tile caminable
        for y in range(height):
            for x in range(width):
                if self.is_terrain_walkable(self.world_map[y, x].terrain):
                    self.player_world_x = x
                    self.player_world_y = y
                    return self.world_map
        
        # Si no hay terreno caminable, usar posición 0,0
        self.player_world_x = 0
        self.player_world_y = 0
        return self.world_map
    
    def load_local_map(self):
        """
        Carga el mapa local para la posición actual del jugador.
        Usa caché para evitar regeneración innecesaria.
        
        Returns:
            Array 2D de MapTile (mapa local)
        """
        # Calcular región actual (64x64)
        region_x = self.player_world_x // 64
        region_y = self.player_world_y // 64
        
        # Verificar si ya está en caché
        cache_key = (region_x, region_y)
        if cache_key in self.local_map_cache:
            self.current_local_map = self.local_map_cache[cache_key]
            self.cached_region_x = region_x
            self.cached_region_y = region_y
            return self.current_local_map
        
        # Generar y cachear el mapa local
        local_map = self.generator.generate_local_map(
            region_x * 64,  # Convertir región a coordenadas mundiales
            region_y * 64,
            local_width=64,
            local_height=64
        )
        
        self.local_map_cache[cache_key] = local_map
        self.current_local_map = local_map
        self.cached_region_x = region_x
        self.cached_region_y = region_y
        
        # Limpiar cache antiguo (mantener solo 9 regiones cercanas)
        if len(self.local_map_cache) > 9:
            keys_to_remove = []
            for key in self.local_map_cache.keys():
                kx, ky = key
                if abs(kx - region_x) > 1 or abs(ky - region_y) > 1:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove[:len(keys_to_remove) - 5]:  # Mantener al menos 5
                del self.local_map_cache[key]
        
        return self.current_local_map
    
    def move_player(self, direction):
        """
        Mueve al jugador en una dirección.
        OPTIMIZADO: solo recalcula el mapa local si cambia de región
        
        Args:
            direction: "up", "down", "left", "right", o tupla (dx, dy)
        
        Returns:
            True si el movimiento fue válido, False en caso contrario
        """
        dx, dy = 0, 0
        
        if direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        elif direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1
        elif isinstance(direction, tuple) and len(direction) == 2:
            dx, dy = direction
        else:
            return False
        
        # Calcular nueva posición
        new_x = self.player_world_x + dx
        new_y = self.player_world_y + dy
        
        # Validar límites del mapa
        if self.world_map is None:
            return False
        
        height, width = self.world_map.shape
        
        if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
            return False
        
        # Verificar si el terreno es navegable
        tile = self.world_map[new_y, new_x]
        if not self.is_terrain_walkable(tile.terrain):
            return False
        
        # Actualizar posición
        self.player_world_x = new_x
        self.player_world_y = new_y
        
        # OPTIMIZACIÓN: solo recalcular si cambia de región (64x64)
        new_region_x = new_x // 64
        new_region_y = new_y // 64
        old_region_x = (new_x - dx) // 64
        old_region_y = (new_y - dy) // 64
        
        if new_region_x != old_region_x or new_region_y != old_region_y:
            # Cambió de región, actualizar mapa local
            self.load_local_map()
        
        return True
    
    @staticmethod
    def is_terrain_walkable(terrain):
        """
        Determina si un terreno es caminable.
        
        Args:
            terrain: Terrain enum
        
        Returns:
            True si es caminable
        """
        non_walkable = [
            Terrain.DEEP_OCEAN,
            Terrain.OCEAN,
            Terrain.DEEP_CHASM,
        ]
        return terrain not in non_walkable
    
    def get_current_terrain_info(self):
        """
        Obtiene información del terreno actual del jugador.
        
        Returns:
            Diccionario con información del terreno
        """
        if self.world_map is None:
            return None
        
        tile = self.world_map[self.player_world_y, self.player_world_x]
        
        return {
            "position": (self.player_world_x, self.player_world_y),
            "terrain_type": tile.terrain.name,
            "terrain_name": tile.get_terrain_name(),
            "height": tile.height,
            "temperature": tile.temperature,
            "temperature_category": tile.get_temperature_category().value,
            "color": tile.get_color(),
        }
    
    def get_nearby_terrain_info(self, radius=1):
        """
        Obtiene información de terrenos cercanos.
        
        Args:
            radius: Radio de búsqueda en celdas
        
        Returns:
            Diccionario con información de terrenos cercanos
        """
        if self.world_map is None:
            return {}
        
        height, width = self.world_map.shape
        nearby = {}
        
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                
                check_x = self.player_world_x + dx
                check_y = self.player_world_y + dy
                
                if 0 <= check_x < width and 0 <= check_y < height:
                    tile = self.world_map[check_y, check_x]
                    key = f"({dx:+d},{dy:+d})"
                    nearby[key] = {
                        "terrain": tile.terrain.name,
                        "name": tile.get_terrain_name(),
                        "walkable": self.is_terrain_walkable(tile.terrain),
                    }
        
        return nearby
    
    def save_game(self, save_path=None):
        """
        Guarda el estado del juego.
        
        Args:
            save_path: Ruta del archivo de guardado (opcional, usa sesión si no se proporciona)
        """
        if save_path is None:
            # Crear ruta automática basada en la sesión
            session_dir = Path(__file__).parent.parent.parent / "saves" / "games" / self.session_name
            session_dir.mkdir(parents=True, exist_ok=True)
            save_path = session_dir / "save.json"
        
        save_data = {
            "world": {
                "seed": self.seed,
                "player_position": {
                    "x": self.player_world_x,
                    "y": self.player_world_y,
                }
            },
            "player": self.player_data if self.player_data else {},
            "session_name": self.session_name
        }
        
        save_file = Path(save_path)
        save_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)
    
    def load_game(self, save_path=None):
        """
        Carga el estado del juego.
        
        Args:
            save_path: Ruta del archivo de guardado (opcional, usa sesión si no se proporciona)
        
        Returns:
            True si se cargó correctamente
        """
        if save_path is None:
            # Crear ruta automática basada en la sesión
            session_dir = Path(__file__).parent.parent.parent / "saves" / "games" / self.session_name
            save_path = session_dir / "save.json"
        
        try:
            with open(save_path, "r", encoding="utf-8") as f:
                save_data = json.load(f)
            
            self.seed = save_data["world"]["seed"]
            self.session_name = save_data.get("session_name", self.session_name)
            self.generator = MapGenerator(seed=self.seed, world_size=128)
            
            pos = save_data["world"]["player_position"]
            saved_x = pos["x"]
            saved_y = pos["y"]
            
            self.player_data = save_data.get("player", {})
            
            # Regenerar el mundo con la misma semilla
            self.generate_world()
            
            # Restaurar posición guardada (después de generar mundo)
            self.player_world_x = saved_x
            self.player_world_y = saved_y
            
            self.load_local_map()
            
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    @staticmethod
    def get_session_list():
        """
        Obtiene lista de sesiones guardadas.
        
        Returns:
            Lista de nombres de sesiones disponibles
        """
        games_dir = Path(__file__).parent.parent.parent / "saves" / "games"
        if not games_dir.exists():
            return []
        
        sessions = []
        for session_dir in games_dir.iterdir():
            if session_dir.is_dir() and (session_dir / "save.json").exists():
                sessions.append(session_dir.name)
        
        return sorted(sessions)
