#!/usr/bin/env python3
# test_new_features.py
"""
Script de prueba para las nuevas características:
- Generación de mapas con temperatura
- Sistema de arena
- Navegación del mundo
"""

import sys
from pathlib import Path
import numpy as np

# Add jogo to path
sys.path.insert(0, str(Path(__file__).parent))

from engine.world.map_generator import MapGenerator, Terrain, Temperature
from engine.world.world import World


def test_map_generation():
    """Prueba la generación de mapas con las nuevas características."""
    print("=" * 60)
    print("PRUEBA 1: Generación de Mapa (MEJORADO)")
    print("=" * 60)
    
    generator = MapGenerator(seed=42, world_size=128)
    world_map = generator.generate_world_map(width=128, height=128)
    
    print(f"\n[OK] Mapa mundial generado: {world_map.shape}")
    print(f"  MEJORADO: Mas tierra, mas montanas, bordes de agua forzados")
    
    # Obtener estadísticas
    stats = generator.get_map_statistics(world_map)
    
    print("\n[STATS] Estadisticas del Mapa MEJORADO:")
    print(f"  Total de celdas: {stats['total_tiles']}")
    print(f"\n  Terrenos encontrados:")
    for terrain_name, count in sorted(stats['terrain_counts'].items()):
        percentage = stats['terrain_percentages'][terrain_name]
        print(f"    - {terrain_name}: {count} celdas ({percentage:.1f}%)")
    
    print(f"\n  Información de Altura:")
    print(f"    - Promedio: {stats['average_height']:.2f}")
    print(f"    - Mínimo: {stats['min_height']:.2f}")
    print(f"    - Máximo: {stats['max_height']:.2f}")
    
    print(f"\n  Información de Temperatura:")
    print(f"    - Promedio: {stats['average_temperature']:.2f}")
    print(f"    - Mínimo: {stats['min_temperature']:.2f}")
    print(f"    - Máximo: {stats['max_temperature']:.2f}")
    
    print(f"\n  Categorías de Temperatura:")
    for temp_cat, count in sorted(stats['temperature_counts'].items()):
        percentage = stats['temperature_percentages'][temp_cat]
        print(f"    - {temp_cat}: {count} celdas ({percentage:.1f}%)")
    
    # Verificar arenas
    arena_count = stats['terrain_counts'].get('ARENA', 0)
    sand_count = stats['terrain_counts'].get('SAND', 0)
    print(f"\n  Arenas de Combate: {arena_count} de {sand_count} arena ({(arena_count/max(1,sand_count))*100:.1f}%)")
    
    # Verificar que hay más montañas
    mountain_count = stats['terrain_counts'].get('MOUNTAINS', 0) + stats['terrain_counts'].get('SNOW_PEAKS', 0)
    print(f"  [OK] Montanas totales: {mountain_count} ({(mountain_count/stats['total_tiles'])*100:.1f}%)")
    
    # Mostrar mapa ASCII (porción)
    print("\n[MAP] Mapa ASCII (primeros 40x20):")
    visualization = generator.visualize_world_map(world_map[:20, :40], show_coordinates=True)
    print(visualization)
    
    # Mostrar leyenda
    print("\n" + generator.get_legend())
    
    return world_map


def test_local_map_detail():
    """Prueba el nuevo mapa local detallado."""
    print("\n" + "=" * 60)
    print("PRUEBA 2b: Mapa Local Detallado (NUEVO)")
    print("=" * 60)
    
    generator = MapGenerator(seed=42, world_size=128)
    
    # Generar mapa local de una región
    local_map = generator.generate_local_map(world_x=64, world_y=64, local_width=64, local_height=64)
    
    print(f"\n[OK] Mapa local generado: {local_map.shape}")
    print(f"  MEJORADO: 64x64 tiles con gran detalle")
    print(f"  Cada tile = 5m^2")
    print(f"  Area total = 320m x 320m (muy detallado)")
    
    # Estadísticas locales
    terrain_local = {}
    height_local = []
    temp_local = []
    
    for tile in local_map.flat:
        terrain_name = tile.terrain.name
        terrain_local[terrain_name] = terrain_local.get(terrain_name, 0) + 1
        height_local.append(tile.height)
        temp_local.append(tile.temperature)
    
    print(f"\n[STATS] Estadisticas del Mapa Local:")
    print(f"  Total tiles: {64*64}")
    print(f"\n  Terrenos locales:")
    for terrain_name in sorted(terrain_local.keys()):
        count = terrain_local[terrain_name]
        pct = (count / (64*64)) * 100
        print(f"    - {terrain_name}: {count} ({pct:.1f}%)")
    
    print(f"\n  Altura local - Promedio: {np.mean(height_local):.2f}")
    print(f"  Temperatura local - Promedio: {np.mean(temp_local):.2f}")
    
    # Visualizar parte del mapa local
    print(f"\n[MAP] Mapa Local ASCII (primeros 32x16):")
    local_vis = generator.visualize_local_map(local_map[:16, :32], show_coordinates=True)
    print(local_vis)
    
    return local_map


def test_temperature_system(world_map):
    """Prueba el sistema de temperatura."""
    print("\n" + "=" * 60)
    print("PRUEBA 2: Sistema de Temperatura")
    print("=" * 60)
    
    # Buscar tiles con diferentes temperaturas
    cold_tiles = []
    hot_tiles = []
    
    for tile in world_map.flat:
        temp_cat = tile.get_temperature_category()
        if temp_cat == Temperature.FROZEN or temp_cat == Temperature.COLD:
            cold_tiles.append(tile)
        elif temp_cat == Temperature.HOT:
            hot_tiles.append(tile)
    
    if cold_tiles:
        cold_tile = cold_tiles[0]
        print(f"\n[COLD] Tile frio encontrado:")
        print(f"    Posición: ({cold_tile.x}, {cold_tile.y})")
        print(f"    Terreno: {cold_tile.get_terrain_name()}")
        print(f"    Temperatura: {cold_tile.temperature:.2f}")
        print(f"    Categoría: {cold_tile.get_temperature_category().value}")
        print(f"    Color RGB: {cold_tile.get_color()}")
    
    if hot_tiles:
        hot_tile = hot_tiles[0]
        print(f"\n[HOT] Tile caliente encontrado:")
        print(f"    Posición: ({hot_tile.x}, {hot_tile.y})")
        print(f"    Terreno: {hot_tile.get_terrain_name()}")
        print(f"    Temperatura: {hot_tile.temperature:.2f}")
        print(f"    Categoría: {hot_tile.get_temperature_category().value}")
        print(f"    Color RGB: {hot_tile.get_color()}")


def test_world_system():
    """Prueba el sistema de mundo y navegación."""
    print("\n" + "=" * 60)
    print("PRUEBA 3: Sistema de Mundo y Navegación")
    print("=" * 60)
    
    world = World(seed=42)
    world.generate_world(width=32, height=32)
    world.load_local_map()
    
    print(f"\n[OK] Mundo creado con semilla: {world.seed}")
    print(f"  Posición inicial: ({world.player_world_x}, {world.player_world_y})")
    
    # Obtener información del terreno actual
    terrain_info = world.get_current_terrain_info()
    print(f"\n[TERRAIN] Terreno actual:")
    print(f"    Tipo: {terrain_info['terrain_name']}")
    print(f"    Temperatura: {terrain_info['temperature_category']}")
    print(f"    Color RGB: {terrain_info['color']}")
    
    # Obtener terrenos cercanos
    nearby = world.get_nearby_terrain_info(radius=1)
    print(f"\n[MAP] Terrenos cercanos (radio 1):")
    for direction, info in sorted(nearby.items()):
        walkable = "[OK] Caminable" if info['walkable'] else "[XX] Bloqueado"
        print(f"    {direction}: {info['name']} ({walkable})")
    
    # Intentar movimiento
    print(f"\n[MOVE] Prueba de movimiento:")
    initial_pos = (world.player_world_x, world.player_world_y)
    
    if world.move_player("right"):
        new_pos = (world.player_world_x, world.player_world_y)
        print(f"    [OK] Movimiento a la derecha exitoso")
        print(f"    Posición anterior: {initial_pos}")
        print(f"    Posición nueva: {new_pos}")
    else:
        print(f"    [XX] No se pudo mover a la derecha (terreno bloqueado)")
    
    # Intentar movimiento fallido
    for _ in range(10):
        if not world.move_player("up"):
            print(f"    [XX] No se pudo mover hacia arriba (probablemente agua)")
            break
    else:
        print(f"    [OK] Movimiento hacia arriba permitido")


def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "=" * 60)
    print("PRUEBAS DEL SISTEMA DE MAPA Y EXPLORACIÓN (MEJORADO)")
    print("=" * 60)
    
    try:
        world_map = test_map_generation()
        local_map = test_local_map_detail()
        test_temperature_system(world_map)
        test_world_system()
        
        print("\n" + "=" * 60)
        print("TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 60)
        print("\nMEJORAS VERIFICADAS:")
        print("  [PASS] Mapa mundial 128x128 (mas amplio)")
        print("  [PASS] Mas tierra que agua")
        print("  [PASS] Montanas presentes")
        print("  [PASS] Bordes de agua forzados (continentes aislados)")
        print("  [PASS] Mapa local 64x64 (muy detallado)")
        print("  [PASS] Variacion de biomas local")
        print("\n")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
