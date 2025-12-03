# engine/world/map_generator.py
"""
Generador de mapas del mundo utilizando Perlin Noise.
Soporta dos niveles de escala:
- Mapa mundial: bloques de 1km
- Mapa local: bloques de 5m
"""

from perlin_noise import PerlinNoise
import numpy as np
from dataclasses import dataclass
from enum import Enum


class Terrain(Enum):
    """Tipos de terreno según altura."""
    # Agua
    DEEP_OCEAN = -1          # < -0.6
    OCEAN = 0                # -0.6 a -0.2
    SHALLOW_WATER = 1        # -0.2 a 0.0
    
    # Tierra
    SAND = 2                 # 0.0 a 0.1
    GRASS = 3                # 0.1 a 0.3
    FOREST = 4               # 0.3 a 0.5
    MOUNTAINS = 5            # 0.5 a 0.7
    SNOW_PEAKS = 6           # > 0.7
    
    # Grietas profundas (solo en local)
    DEEP_CHASM = 7           # < -0.8


class TerrainColor(Enum):
    """Colores para visualización."""
    DEEP_OCEAN = "🌊"        # Azul profundo
    OCEAN = "🌊"
    SHALLOW_WATER = "💧"
    SAND = "🟨"
    GRASS = "🟩"
    FOREST = "🟩"
    MOUNTAINS = "🏔️"
    SNOW_PEAKS = "⛰️"
    DEEP_CHASM = "⬛"
    
    # Alternativas en blanco/negro si los emojis no funcionan
    DEEP_OCEAN_ALT = "~"
    OCEAN_ALT = "~"
    SHALLOW_WATER_ALT = "."
    SAND_ALT = "s"
    GRASS_ALT = "g"
    FOREST_ALT = "f"
    MOUNTAINS_ALT = "^"
    SNOW_PEAKS_ALT = "A"
    DEEP_CHASM_ALT = "#"


@dataclass
class MapTile:
    """Representa una celda del mapa."""
    x: int
    y: int
    height: float  # -1.0 a 1.0
    terrain: Terrain
    
    def __str__(self):
        """Retorna representación visual del terreno."""
        if self.terrain == Terrain.DEEP_OCEAN:
            return TerrainColor.DEEP_OCEAN.value
        elif self.terrain == Terrain.OCEAN:
            return TerrainColor.OCEAN.value
        elif self.terrain == Terrain.SHALLOW_WATER:
            return TerrainColor.SHALLOW_WATER.value
        elif self.terrain == Terrain.SAND:
            return TerrainColor.SAND.value
        elif self.terrain == Terrain.GRASS:
            return TerrainColor.GRASS.value
        elif self.terrain == Terrain.FOREST:
            return TerrainColor.FOREST.value
        elif self.terrain == Terrain.MOUNTAINS:
            return TerrainColor.MOUNTAINS.value
        elif self.terrain == Terrain.SNOW_PEAKS:
            return TerrainColor.SNOW_PEAKS.value
        elif self.terrain == Terrain.DEEP_CHASM:
            return TerrainColor.DEEP_CHASM.value
        return "?"


class MapGenerator:
    """Generador de mapas usando Perlin Noise."""
    
    def __init__(self, seed=42):
        """
        Inicializa el generador.
        
        Args:
            seed: Semilla para reproducibilidad
        """
        self.seed = seed
        self.world_noise = None
        self.local_noise = None
        self.init_noise()
    
    def init_noise(self):
        """Inicializa los generadores de Perlin Noise."""
        # Usar semilla para reproducibilidad
        np.random.seed(self.seed)
        
        # Mapa mundial (escala grande, 1km por celda)
        self.world_noise = PerlinNoise(octaves=4, seed=self.seed)
        
        # Mapa local (escala pequeña, 5m por celda)
        self.local_noise = PerlinNoise(octaves=8, seed=self.seed + 1000)
    
    def get_terrain_type(self, height, is_local=False):
        """
        Determina el tipo de terreno según la altura.
        
        Args:
            height: Valor de altura normalizado (-1.0 a 1.0)
            is_local: True si es mapa local, False si es mundial
        
        Returns:
            Terrain enum
        """
        # En mapa local, permitir grietas profundas
        if is_local and height < -0.8:
            return Terrain.DEEP_CHASM
        
        if height < -0.6:
            return Terrain.DEEP_OCEAN
        elif height < -0.2:
            return Terrain.OCEAN
        elif height < 0.0:
            return Terrain.SHALLOW_WATER
        elif height < 0.1:
            return Terrain.SAND
        elif height < 0.3:
            return Terrain.GRASS
        elif height < 0.5:
            return Terrain.FOREST
        elif height < 0.7:
            return Terrain.MOUNTAINS
        else:
            return Terrain.SNOW_PEAKS
    
    def generate_world_map(self, width=64, height=64):
        """
        Genera el mapa mundial.
        
        Args:
            width: Ancho del mapa en celdas (1km cada una)
            height: Alto del mapa en celdas (1km cada una)
        
        Returns:
            Array 2D de MapTile
        """
        world_map = np.empty((height, width), dtype=object)
        
        # Escala para el ruido mundial
        scale = 50  # Controla la "zoom" del ruido
        
        for y in range(height):
            for x in range(width):
                # Generar valor de Perlin Noise
                # Usar tupla de coordenadas
                noise_val = self.world_noise([x / scale, y / scale])
                
                # Normalizar a -1.0 a 1.0
                height_val = max(-1.0, min(1.0, noise_val))
                
                # Determinar terreno
                terrain = self.get_terrain_type(height_val, is_local=False)
                
                # Crear celda
                world_map[y, x] = MapTile(x, y, height_val, terrain)
        
        return world_map
    
    def generate_local_map(self, world_x, world_y, local_width=32, local_height=32):
        """
        Genera el mapa local para una región del mundo.
        Cada celda del mapa mundial expande a local_width x local_height celdas locales.
        
        Args:
            world_x: Coordenada X en el mapa mundial
            world_y: Coordenada Y en el mapa mundial
            local_width: Ancho del mapa local en celdas (5m cada una)
            local_height: Alto del mapa local en celdas (5m cada una)
        
        Returns:
            Array 2D de MapTile
        """
        local_map = np.empty((local_height, local_width), dtype=object)
        
        # Escala para el ruido local
        # Más octavas = más detalle
        local_scale = 15  # Más pequeño = más detalle
        
        # Offset global basado en posición mundial
        global_offset_x = world_x * 100  # 100 celdas locales por celda mundial
        global_offset_y = world_y * 100
        
        for y in range(local_height):
            for x in range(local_width):
                # Generar valor de Perlin Noise local
                noise_x = (global_offset_x + x) / local_scale
                noise_y = (global_offset_y + y) / local_scale
                
                noise_val = self.local_noise([noise_x, noise_y])
                
                # Normalizar a -1.0 a 1.0
                height_val = max(-1.0, min(1.0, noise_val))
                
                # Determinar terreno (permite grietas profundas)
                terrain = self.get_terrain_type(height_val, is_local=True)
                
                # Crear celda local
                local_map[y, x] = MapTile(
                    world_x * local_width + x,
                    world_y * local_height + y,
                    height_val,
                    terrain
                )
        
        return local_map
    
    def visualize_world_map(self, world_map, show_coordinates=False):
        """
        Visualiza el mapa mundial como ASCII art.
        
        Args:
            world_map: Array 2D de MapTile
            show_coordinates: Si True, muestra coordenadas
        
        Returns:
            String con visualización
        """
        height, width = world_map.shape
        result = []
        
        if show_coordinates:
            # Mostrar números de columna
            col_header = "    " + "".join(f"{i%10}" for i in range(width))
            result.append(col_header)
        
        for y in range(height):
            if show_coordinates:
                row = f"{y:3d} "
            else:
                row = ""
            
            for x in range(width):
                tile = world_map[y, x]
                row += str(tile)
            
            result.append(row)
        
        return "\n".join(result)
    
    def visualize_local_map(self, local_map, show_coordinates=False, show_heights=False):
        """
        Visualiza el mapa local como ASCII art.
        
        Args:
            local_map: Array 2D de MapTile
            show_coordinates: Si True, muestra coordenadas
            show_heights: Si True, muestra valores de altura
        
        Returns:
            String con visualización
        """
        height, width = local_map.shape
        result = []
        
        if show_coordinates:
            col_header = "    " + "".join(f"{i%10}" for i in range(width))
            result.append(col_header)
        
        for y in range(height):
            if show_coordinates:
                row = f"{y:3d} "
            else:
                row = ""
            
            for x in range(width):
                tile = local_map[y, x]
                
                if show_heights:
                    # Mostrar altura como número
                    height_char = str(int(tile.height * 9))
                else:
                    height_char = str(tile)
                
                row += height_char
            
            result.append(row)
        
        return "\n".join(result)
    
    def get_map_statistics(self, world_map):
        """
        Calcula estadísticas del mapa.
        
        Args:
            world_map: Array 2D de MapTile
        
        Returns:
            Diccionario con estadísticas
        """
        height, width = world_map.shape
        total = height * width
        
        terrain_counts = {}
        height_values = []
        
        for y in range(height):
            for x in range(width):
                tile = world_map[y, x]
                terrain_name = tile.terrain.name
                terrain_counts[terrain_name] = terrain_counts.get(terrain_name, 0) + 1
                height_values.append(tile.height)
        
        # Calcular porcentajes
        terrain_percentages = {
            name: (count / total) * 100 
            for name, count in terrain_counts.items()
        }
        
        return {
            "total_tiles": total,
            "terrain_counts": terrain_counts,
            "terrain_percentages": terrain_percentages,
            "average_height": np.mean(height_values),
            "min_height": np.min(height_values),
            "max_height": np.max(height_values),
        }
