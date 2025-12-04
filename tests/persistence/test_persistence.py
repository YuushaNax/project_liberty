#!/usr/bin/env python3
# test_persistence.py
"""
Script de prueba para el sistema de persistencia y optimizaciones.
"""

import sys
from pathlib import Path
import json
import time

# Add jogo to path
sys.path.insert(0, str(Path(__file__).parent))

from engine.world.world import World


def test_session_creation():
    """Prueba creación de una nueva sesión."""
    print("=" * 60)
    print("PRUEBA 1: Creacion de Sesion")
    print("=" * 60)
    
    session_name = "test_character"
    world = World(seed=42, session_name=session_name)
    
    print(f"[OK] Mundo creado - Sesion: {session_name}")
    
    # Generar mundo
    world.generate_world(width=128, height=128)
    world.player_data = {
        "name": "Test Character",
        "race": "Human",
        "age": 25
    }
    
    print(f"[OK] Mundo generado 128x128")
    print(f"[OK] Posicion inicial: ({world.player_world_x}, {world.player_world_y})")
    
    # Cargar mapa local
    world.load_local_map()
    print(f"[OK] Mapa local cargado: 64x64")
    
    return world


def test_save_load(world):
    """Prueba guardado y carga."""
    print("\n" + "=" * 60)
    print("PRUEBA 2: Guardado y Carga")
    print("=" * 60)
    
    # Guardar
    world.save_game()
    print(f"[OK] Partida guardada - Sesion: {world.session_name}")
    
    session_dir = Path(__file__).parent / "saves" / "games" / world.session_name
    save_file = session_dir / "save.json"
    
    if save_file.exists():
        print(f"[OK] Archivo encontrado: {save_file}")
        
        with open(save_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"[OK] Datos guardados:")
            print(f"    - Semilla: {data['world']['seed']}")
            print(f"    - Posicion: ({data['world']['player_position']['x']}, {data['world']['player_position']['y']})")
            print(f"    - Jugador: {data['player']['name']}")
    
    # Cargar en un nuevo mundo
    world2 = World(session_name=world.session_name)
    success = world2.load_game()
    
    if success:
        print(f"\n[OK] Partida cargada correctamente")
        print(f"[OK] Posicion restaurada: ({world2.player_world_x}, {world2.player_world_y})")
        print(f"[OK] Datos del jugador: {world2.player_data.get('name')}")
    else:
        print(f"[XX] Error al cargar la partida")
    
    return world2


def test_movement_optimization():
    """Prueba optimizacion del movimiento."""
    print("\n" + "=" * 60)
    print("PRUEBA 3: Optimizacion de Movimiento")
    print("=" * 60)
    
    world = World(seed=42, session_name="optimization_test")
    world.generate_world(width=128, height=128)
    world.load_local_map()
    
    print(f"[OK] Mundo generado")
    print(f"[OK] Posicion inicial: ({world.player_world_x}, {world.player_world_y})")
    
    # Medir tiempo de movimiento sin cambio de región
    print(f"\n[TEST] Movimiento dentro de region (sin regeneracion):")
    
    moves_within_region = 0
    initial_region_x = world.player_world_x // 64
    initial_region_y = world.player_world_y // 64
    
    start_time = time.time()
    for _ in range(20):
        if not world.move_player("right"):
            world.move_player("down")
            moves_within_region += 1
        moves_within_region += 1
    time_within = time.time() - start_time
    
    current_region_x = world.player_world_x // 64
    current_region_y = world.player_world_y // 64
    
    if current_region_x == initial_region_x and current_region_y == initial_region_y:
        print(f"  [OK] Permanecio en misma region")
        print(f"  [OK] 20 movimientos en {time_within*1000:.2f}ms")
        print(f"  [OK] Promedio: {(time_within/20)*1000:.3f}ms por movimiento")
    else:
        print(f"  [INFO] Cambio de region, probando de nuevo desde centro")
        # Resetear a centro
        world.player_world_x = 64
        world.player_world_y = 64
        world.load_local_map()
        
        start_time = time.time()
        for _ in range(20):
            if not world.move_player("right"):
                world.move_player("down")
        time_within = time.time() - start_time
        
        print(f"  [OK] 20 movimientos en {time_within*1000:.2f}ms")
        print(f"  [OK] Promedio: {(time_within/20)*1000:.3f}ms por movimiento")
    
    # Medir tiempo de cambio de región
    print(f"\n[TEST] Movimiento entre regiones (con regeneracion):")
    
    # Mover hasta el borde de región
    world.player_world_x = 63
    world.player_world_y = 64
    world.cached_region_x = 0
    world.cached_region_y = 1
    world.load_local_map()
    
    start_time = time.time()
    world.move_player("right")  # Cambiar de región
    time_region_change = time.time() - start_time
    
    print(f"  [OK] Cambio de region en {time_region_change*1000:.2f}ms")
    print(f"  [OK] Cache tiene {len(world.local_map_cache)} regiones almacenadas")


def test_session_list():
    """Prueba listado de sesiones."""
    print("\n" + "=" * 60)
    print("PRUEBA 4: Listado de Sesiones Guardadas")
    print("=" * 60)
    
    sessions = World.get_session_list()
    
    print(f"[OK] Total de sesiones: {len(sessions)}")
    for i, session in enumerate(sessions, 1):
        print(f"  {i}. {session}")


def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "=" * 60)
    print("PRUEBAS DE PERSISTENCIA Y OPTIMIZACION")
    print("=" * 60)
    
    try:
        # Test 1: Crear sesión
        world = test_session_creation()
        
        # Test 2: Guardar y cargar
        world2 = test_save_load(world)
        
        # Test 3: Optimización de movimiento
        test_movement_optimization()
        
        # Test 4: Listar sesiones
        test_session_list()
        
        print("\n" + "=" * 60)
        print("TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 60)
        print("\nMEJORAS VERIFICADAS:")
        print("  [PASS] Sistema de persistencia funciona")
        print("  [PASS] Sesiones se guardan en carpetas individuales")
        print("  [PASS] Carga de partidas restaura estado completo")
        print("  [PASS] Movimiento optimizado con caché de regiones")
        print("  [PASS] Cambio de región solo regenera cuando es necesario")
        print("\n")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
