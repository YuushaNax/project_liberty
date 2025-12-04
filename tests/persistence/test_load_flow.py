#!/usr/bin/env python3
# test_load_flow.py
"""
Prueba el flujo de carga de partida sin interfaz gráfica.
"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from engine.world.world import World


def test_load_flow():
    """Prueba el flujo de carga."""
    print("=" * 60)
    print("PRUEBA: Flujo de Carga de Partida")
    print("=" * 60)
    
    # Obtener sesiones guardadas
    sessions = World.get_session_list()
    print(f"\n[OK] Sesiones disponibles: {len(sessions)}")
    for session in sessions:
        print(f"  - {session}")
    
    if not sessions:
        print("[XX] No hay sesiones guardadas para cargar")
        return
    
    # Cargar primera sesión
    session_name = sessions[0]
    print(f"\n[TEST] Cargando sesión: {session_name}")
    
    world = World(session_name=session_name)
    
    # Verificar que el archivo existe
    session_dir = Path(__file__).parent / "saves" / "games" / session_name
    save_file = session_dir / "save.json"
    
    if not save_file.exists():
        print(f"[XX] Archivo no encontrado: {save_file}")
        return
    
    print(f"[OK] Archivo encontrado: {save_file}")
    
    # Leer contenido
    with open(save_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"[OK] Contenido del archivo:")
    print(f"  - Seed: {data['world']['seed']}")
    print(f"  - Posición: ({data['world']['player_position']['x']}, {data['world']['player_position']['y']})")
    print(f"  - Jugador: {data['player'].get('name', 'Unknown')}")
    
    # Cargar
    print(f"\n[TEST] Llamando a world.load_game()...")
    success = world.load_game()
    
    if success:
        print(f"[OK] Partida cargada correctamente")
        print(f"  - Seed: {world.seed}")
        print(f"  - Posición: ({world.player_world_x}, {world.player_world_y})")
        print(f"  - Datos jugador: {world.player_data}")
        print(f"\n✅ PRUEBA EXITOSA")
    else:
        print(f"[XX] Error al cargar la partida")


if __name__ == "__main__":
    test_load_flow()
