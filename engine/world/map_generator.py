# engine/world/map_generator.py
"""
Generador de mapas del mundo utilizando Perlin Noise.
Soporta dos niveles de escala:
- Mapa mundial: bloques de 1km
- Mapa local: bloques de 5m

Características:
- Temperature layer con Perlin noise adicional
- Arenas solo en desiertos y playas
- Montañas volcánicas (calientes) y nevadas (frías)
- Sistema de colores para visualización en pygame
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
    SAND = 2                 # 0.0 a 0.1 (desierto/playa)
    GRASS = 3                # 0.1 a 0.3
    FOREST = 4               # 0.3 a 0.5
    MOUNTAINS = 5            # 0.5 a 0.7
    SNOW_PEAKS = 6           # > 0.7
    
    # Estructuras especiales
    ARENA = 7                # Especial - solo en desiertos/playas
    
    # Grietas profundas (solo en local)
    DEEP_CHASM = 8           # < -0.8


class Temperature(Enum):
    """Clasificación de temperatura."""
    FROZEN = "frozen"        # < -0.5
    COLD = "cold"            # -0.5 a -0.1
    COOL = "cool"            # -0.1 a 0.2
    TEMPERATE = "temperate"  # 0.2 a 0.5
    WARM = "warm"            # 0.5 a 0.8
    HOT = "hot"              # > 0.8


class TerrainColor(Enum):
    """Colores RGB para visualización en pygame."""
    # Agua
    DEEP_OCEAN = (0, 20, 60)
    OCEAN = (20, 80, 150)
    SHALLOW_WATER = (100, 150, 200)
    
    # Tierra - variaciones según temperatura
    SAND_COOL = (180, 160, 100)      # Arena fría (gris-arena)
    SAND_TEMPERATE = (210, 180, 80)  # Arena templada
    SAND_HOT = (240, 200, 60)        # Arena caliente (más dorada)
    
    GRASS_COOL = (80, 120, 60)       # Hierba fría
    GRASS_TEMPERATE = (100, 180, 80) # Hierba templada
    GRASS_HOT = (120, 200, 60)       # Hierba caliente
    
    FOREST_COOL = (40, 80, 40)       # Bosque frío (oscuro)
    FOREST_TEMPERATE = (60, 120, 40) # Bosque templado
    FOREST_HOT = (80, 140, 50)       # Bosque tropical
    
    # Montañas
    MOUNTAINS_COLD = (150, 150, 180) # Montañas nevadas
    MOUNTAINS_VOLCANIC = (120, 60, 20) # Montañas volcánicas (marrones)
    MOUNTAINS_TEMPERATE = (140, 100, 60) # Montañas templadas
    
    SNOW_PEAKS = (240, 240, 255)     # Picos nevados
    
    # Especial
    ARENA = (200, 140, 40)           # Arena de lucha
    DEEP_CHASM = (40, 20, 30)        # Grieta profunda
    
    # Marcador de jugador
    PLAYER = (255, 215, 0)           # Dorado


@dataclass
class MapTile:
    """Representa una celda del mapa."""
    x: int
    y: int
    height: float  # -1.0 a 1.0
    terrain: Terrain
    temperature: float = 0.0  # -1.0 (frío) a 1.0 (caliente)
    
    def get_terrain_name(self):
        """Retorna nombre del terreno en español."""
        names = {
            Terrain.DEEP_OCEAN: "Océano Profundo",
            Terrain.OCEAN: "Océano",
            Terrain.SHALLOW_WATER: "Agua Poco Profunda",
            Terrain.SAND: "Arena",
            Terrain.GRASS: "Hierba",
            Terrain.FOREST: "Bosque",
            Terrain.MOUNTAINS: "Montaña",
            Terrain.SNOW_PEAKS: "Picos Nevados",
            Terrain.ARENA: "Arena de Combate",
            Terrain.DEEP_CHASM: "Grieta Profunda",
        }
        return names.get(self.terrain, "Desconocido")
    
    def get_temperature_category(self):
        """Retorna categoría de temperatura."""
        if self.temperature < -0.5:
            return Temperature.FROZEN
        elif self.temperature < -0.1:
            return Temperature.COLD
        elif self.temperature < 0.2:
            return Temperature.COOL
        elif self.temperature < 0.5:
            return Temperature.TEMPERATE
        elif self.temperature < 0.8:
            return Temperature.WARM
        else:
            return Temperature.HOT
    
    def get_color(self):
        """Retorna color RGB para este tile según terreno y temperatura."""
        temp_cat = self.get_temperature_category()
        
        # Agua (sin variación de temperatura visual)
        if self.terrain == Terrain.DEEP_OCEAN:
            return TerrainColor.DEEP_OCEAN.value
        elif self.terrain == Terrain.OCEAN:
            return TerrainColor.OCEAN.value
        elif self.terrain == Terrain.SHALLOW_WATER:
            return TerrainColor.SHALLOW_WATER.value
        
        # Arena con variación de temperatura
        elif self.terrain == Terrain.SAND:
            if temp_cat in (Temperature.FROZEN, Temperature.COLD, Temperature.COOL):
                return TerrainColor.SAND_COOL.value
            elif temp_cat == Temperature.TEMPERATE:
                return TerrainColor.SAND_TEMPERATE.value
            else:
                return TerrainColor.SAND_HOT.value
        
        # Hierba con variación de temperatura
        elif self.terrain == Terrain.GRASS:
            if temp_cat in (Temperature.FROZEN, Temperature.COLD, Temperature.COOL):
                return TerrainColor.GRASS_COOL.value
            elif temp_cat == Temperature.TEMPERATE:
                return TerrainColor.GRASS_TEMPERATE.value
            else:
                return TerrainColor.GRASS_HOT.value
        
        # Bosque con variación de temperatura
        elif self.terrain == Terrain.FOREST:
            if temp_cat in (Temperature.FROZEN, Temperature.COLD, Temperature.COOL):
                return TerrainColor.FOREST_COOL.value
            elif temp_cat == Temperature.TEMPERATE:
                return TerrainColor.FOREST_TEMPERATE.value
            else:
                return TerrainColor.FOREST_HOT.value
        
        # Montañas con variación de temperatura (volcánicas vs nevadas)
        elif self.terrain == Terrain.MOUNTAINS:
            if temp_cat in (Temperature.FROZEN, Temperature.COLD):
                return TerrainColor.MOUNTAINS_COLD.value
            elif temp_cat in (Temperature.WARM, Temperature.HOT):
                return TerrainColor.MOUNTAINS_VOLCANIC.value
            else:
                return TerrainColor.MOUNTAINS_TEMPERATE.value
        
        # Picos nevados
        elif self.terrain == Terrain.SNOW_PEAKS:
            return TerrainColor.SNOW_PEAKS.value
        
        # Arena de combate
        elif self.terrain == Terrain.ARENA:
            return TerrainColor.ARENA.value
        
        # Grieta profunda
        elif self.terrain == Terrain.DEEP_CHASM:
            return TerrainColor.DEEP_CHASM.value
        
        return (200, 200, 200)  # Fallback gray
    
    def get_ascii_char(self):
        """Retorna carácter ASCII para representación en texto."""
        chars = {
            Terrain.DEEP_OCEAN: "~",
            Terrain.OCEAN: "~",
            Terrain.SHALLOW_WATER: ".",
            Terrain.SAND: "s",
            Terrain.GRASS: "g",
            Terrain.FOREST: "f",
            Terrain.MOUNTAINS: "^",
            Terrain.SNOW_PEAKS: "A",
            Terrain.ARENA: "@",
            Terrain.DEEP_CHASM: "#",
        }
        return chars.get(self.terrain, "?")


class MapGenerator:
    """Generador de mapas usando Perlin Noise con más tierra y montañas."""
    
    def __init__(self, seed=42, world_size=128):
        """
        Inicializa el generador.
        
        Args:
            seed: Semilla para reproducibilidad
            world_size: Tamaño del mundo (será cuadrado: world_size x world_size)
        """
        self.seed = seed
        self.world_size = world_size
        self.world_noise = None
        self.local_noise = None
        self.temperature_noise = None
        self.mountain_noise = None  # Capa adicional para montañas
        self.init_noise()
    
    def init_noise(self):
        """Inicializa los generadores de Perlin Noise."""
        # Usar semilla para reproducibilidad
        np.random.seed(self.seed)
        
        # Mapa mundial - escala grande para continentes
        # Menos octavas = características más grandes (continentes)
        self.world_noise = PerlinNoise(octaves=3, seed=self.seed)
        
        # Mapa local - más detalle
        self.local_noise = PerlinNoise(octaves=10, seed=self.seed + 1000)
        
        # Capa de temperatura separada
        self.temperature_noise = PerlinNoise(octaves=3, seed=self.seed + 2000)
        
        # Capa adicional para montañas - alta frecuencia
        self.mountain_noise = PerlinNoise(octaves=5, seed=self.seed + 3000)
    
    def get_terrain_type(self, height, mountain_factor=0.0, is_local=False):
        """
        Determina el tipo de terreno según la altura.
        
        Args:
            height: Valor de altura normalizado (-1.0 a 1.0)
            mountain_factor: Factor de influencia de montañas (0.0 a 1.0)
            is_local: True si es mapa local, False si es mundial
        
        Returns:
            Terrain enum
        """
        # En mapa local, permitir grietas profundas
        if is_local and height < -0.85:
            return Terrain.DEEP_CHASM
        
        # Agua profunda - reducida para más tierra
        if height < -0.55:
            return Terrain.DEEP_OCEAN
        elif height < -0.25:
            return Terrain.OCEAN
        elif height < -0.05:
            return Terrain.SHALLOW_WATER
        
        # Tierra - con influencia de montañas
        elif height < 0.15:
            return Terrain.SAND
        elif height < 0.35:
            return Terrain.GRASS
        elif height < 0.55:
            # Bosque - menos probable si hay montañas
            if mountain_factor > 0.3:
                return Terrain.MOUNTAINS
            return Terrain.FOREST
        elif height < 0.75:
            # Montañas - aumentadas
            return Terrain.MOUNTAINS
        else:
            # Picos nevados - más comunes
            return Terrain.SNOW_PEAKS
    
    def should_have_arena(self, terrain, temperature, random_factor):
        """
        Determina si una celda debe tener arena de combate.
        Las arenas solo aparecen en desiertos y playas, con baja probabilidad.
        
        Args:
            terrain: Tipo de terreno
            temperature: Temperatura normalizada
            random_factor: Factor aleatorio (0-1)
        
        Returns:
            True si debe haber arena
        """
        # Las arenas solo pueden estar en SAND
        if terrain != Terrain.SAND:
            return False
        
        # Las arenas son raras (5% de chance en arena)
        if random_factor < 0.05:
            # Preferencia por arena caliente
            if temperature > 0.3:
                return True
        
        return False
    
    def generate_world_map(self, width=None, height=None):
        """
        Genera el mapa mundial con más tierra, montañas y bordes de agua.
        
        Args:
            width: Ancho del mapa en celdas (1km cada una)
            height: Alto del mapa en celdas (1km cada una)
        
        Returns:
            Array 2D de MapTile
        """
        if width is None:
            width = self.world_size
        if height is None:
            height = self.world_size
        
        world_map = np.empty((height, width), dtype=object)
        
        # Escalas para el ruido
        world_scale = 80        # Escala más grande = continentes más grandes
        mountain_scale = 40     # Escala para capas de montaña
        temp_scale = 100        # Escala de temperatura
        
        for y in range(height):
            for x in range(width):
                # === RUIDO DE ALTURA PRINCIPAL ===
                noise_val = self.world_noise([x / world_scale, y / world_scale])
                height_val = max(-1.0, min(1.0, noise_val))
                
                # === CAPA DE MONTAÑAS ADICIONAL ===
                # Añadir variabilidad de montañas
                mountain_val = self.mountain_noise([x / mountain_scale, y / mountain_scale])
                mountain_influence = max(0.0, mountain_val * 0.5)  # Rango 0.0-0.5
                
                # Elevar el terreno general (más tierra que agua)
                # Aplicar booste para tener más tierra
                height_val = height_val * 0.7 + 0.3  # Shiftea hacia positivo
                
                # Añadir influencia de montañas
                height_val = height_val + mountain_influence * 0.3
                
                # === RUIDO DE TEMPERATURA ===
                temp_val = self.temperature_noise([x / temp_scale, y / temp_scale])
                temp_val = max(-1.0, min(1.0, temp_val))
                
                # === FORZAR BORDES DE AGUA ===
                # Crear un "anillo" de agua alrededor del mapa
                border_distance = min(x, y, width - 1 - x, height - 1 - y)
                border_threshold = 5  # Distancia desde el borde
                
                if border_distance < border_threshold:
                    # Gradualmente aumentar agua hacia los bordes
                    water_influence = (border_threshold - border_distance) / border_threshold
                    height_val = height_val * (1.0 - water_influence) - 0.5 * water_influence
                
                # Clampear valores finales
                height_val = max(-1.0, min(1.0, height_val))
                
                # Determinar terreno
                terrain = self.get_terrain_type(height_val, mountain_factor=mountain_influence, is_local=False)
                
                # Posibilidad de arena en lugar de Sand
                import random as rnd
                rnd.seed(self.seed + x * 1000 + y)
                rand_factor = rnd.random()
                
                if self.should_have_arena(terrain, temp_val, rand_factor):
                    terrain = Terrain.ARENA
                
                # Crear celda
                world_map[y, x] = MapTile(x, y, height_val, terrain, temp_val)
        
        return world_map
    
    def generate_local_map(self, world_x, world_y, local_width=64, local_height=64):
        """
        Genera el mapa local para una región del mundo con MUCHO MÁS DETALLE.
        Cada celda del mapa mundial expande a local_width x local_height celdas locales.
        
        Características:
        - Más detalle que el mapa mundial
        - Características más pequeñas visibles
        - Vegetación y detalles varían por bioma
        - Grietas, lagos pequeños, colinas menores
        
        Args:
            world_x: Coordenada X en el mapa mundial
            world_y: Coordenada Y en el mapa mundial
            local_width: Ancho del mapa local en celdas (5m cada una) - aumentado a 64
            local_height: Alto del mapa local en celdas (5m cada una) - aumentado a 64
        
        Returns:
            Array 2D de MapTile
        """
        local_map = np.empty((local_height, local_width), dtype=object)
        
        # Escalas para el ruido local - MÁS DETALLE
        local_scale = 8          # Más pequeño = más variación (antes era 15)
        mountain_local_scale = 5 # Para montañas locales
        temp_local_scale = 15    # Temperatura local
        
        # Offset global basado en posición mundial
        global_offset_x = world_x * 200  # Aumentado para consistencia
        global_offset_y = world_y * 200
        
        # Base de seed determinística
        import random as rnd
        base_seed = self.seed + world_x * 10000 + world_y * 100
        
        for y in range(local_height):
            for x in range(local_width):
                # === ALTURA LOCAL CON GRAN DETALLE ===
                noise_x = (global_offset_x + x) / local_scale
                noise_y = (global_offset_y + y) / local_scale
                noise_val = self.local_noise([noise_x, noise_y])
                height_val = max(-1.0, min(1.0, noise_val))
                
                # === DETALLES DE MONTAÑA A NIVEL LOCAL ===
                mountain_x = (global_offset_x + x) / mountain_local_scale
                mountain_y = (global_offset_y + y) / mountain_local_scale
                mountain_val = self.mountain_noise([mountain_x, mountain_y])
                mountain_influence = max(0.0, mountain_val * 0.4)
                
                # Mezclar influencias
                height_val = height_val * 0.6 + mountain_influence * 0.4
                
                # === TEMPERATURA LOCAL ===
                temp_x = (global_offset_x + x) / temp_local_scale
                temp_y = (global_offset_y + y) / temp_local_scale
                temp_val = self.temperature_noise([temp_x, temp_y])
                temp_val = max(-1.0, min(1.0, temp_val))
                
                # === DETERMINACIÓN DEL TERRENO ===
                # Usar la misma lógica pero con más detalle
                terrain = self.get_terrain_type(height_val, mountain_factor=mountain_influence, is_local=True)
                
                # === ARENAS DE COMBATE (raras pero posibles localmente) ===
                rnd.seed(base_seed + x * 100 + y)
                rand_factor = rnd.random()
                
                if self.should_have_arena(terrain, temp_val, rand_factor):
                    terrain = Terrain.ARENA
                
                # === VARIACIÓN DE TERRENO POR BIOMA ===
                # Añadir más diversidad visual dentro de un bioma
                if terrain == Terrain.GRASS:
                    # Algunos tiles de hierba pueden ser más altos (pequeñas colinas)
                    rnd.seed(base_seed + x * 50 + y * 50)
                    if rnd.random() < 0.15 and height_val > 0.25:
                        # Pequeña colina
                        terrain = Terrain.FOREST
                
                elif terrain == Terrain.FOREST:
                    # Algunos bosques pueden tener claros o ser más densos
                    rnd.seed(base_seed + x * 75 + y * 75)
                    if rnd.random() < 0.1 and height_val > 0.35:
                        # Claro en el bosque
                        terrain = Terrain.GRASS
                
                elif terrain == Terrain.SHALLOW_WATER:
                    # Pequeños lagos pueden tener islas de hierba
                    rnd.seed(base_seed + x * 80 + y * 80)
                    if rnd.random() < 0.08 and height_val > -0.15:
                        terrain = Terrain.SAND
                
                # Crear celda local con coordenadas globales
                local_map[y, x] = MapTile(
                    world_x * local_width + x,
                    world_y * local_height + y,
                    height_val,
                    terrain,
                    temp_val
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
                row += tile.get_ascii_char()
            
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
                    height_char = tile.get_ascii_char()
                
                row += height_char
            
            result.append(row)
        
        return "\n".join(result)
    
    def get_legend(self):
        """
        Retorna una leyenda de terrenos y símbolos.
        
        Returns:
            String con leyenda formateada
        """
        legend_items = [
            ("~", "Océano/Agua"),
            (".", "Agua Poco Profunda"),
            ("s", "Arena/Desierto"),
            ("g", "Hierba/Pradera"),
            ("f", "Bosque"),
            ("^", "Montaña"),
            ("A", "Picos Nevados"),
            ("@", "Arena de Combate"),
            ("#", "Grieta Profunda"),
        ]
        
        result = ["═" * 40, "LEYENDA DEL MAPA", "═" * 40]
        
        for symbol, description in legend_items:
            result.append(f"  {symbol}  →  {description}")
        
        result.append("")
        result.append("TEMPERATURAS:")
        temps = [
            ("Congelado", "< -50°"),
            ("Frío", "-50° a -10°"),
            ("Fresco", "-10° a +20°"),
            ("Templado", "+20° a +50°"),
            ("Cálido", "+50° a +80°"),
            ("Caliente", "> +80°"),
        ]
        for temp_name, temp_range in temps:
            result.append(f"  • {temp_name}: {temp_range}")
        
        result.append("═" * 40)
        
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
        temp_values = []
        temp_category_counts = {}
        
        for y in range(height):
            for x in range(width):
                tile = world_map[y, x]
                terrain_name = tile.terrain.name
                terrain_counts[terrain_name] = terrain_counts.get(terrain_name, 0) + 1
                height_values.append(tile.height)
                temp_values.append(tile.temperature)
                
                # Contar categorías de temperatura
                temp_cat = tile.get_temperature_category()
                temp_name = temp_cat.value
                temp_category_counts[temp_name] = temp_category_counts.get(temp_name, 0) + 1
        
        # Calcular porcentajes
        terrain_percentages = {
            name: (count / total) * 100 
            for name, count in terrain_counts.items()
        }
        
        temp_percentages = {
            name: (count / total) * 100
            for name, count in temp_category_counts.items()
        }
        
        return {
            "total_tiles": total,
            "terrain_counts": terrain_counts,
            "terrain_percentages": terrain_percentages,
            "temperature_counts": temp_category_counts,
            "temperature_percentages": temp_percentages,
            "average_height": np.mean(height_values),
            "min_height": np.min(height_values),
            "max_height": np.max(height_values),
            "average_temperature": np.mean(temp_values),
            "min_temperature": np.min(temp_values),
            "max_temperature": np.max(temp_values),
        }
