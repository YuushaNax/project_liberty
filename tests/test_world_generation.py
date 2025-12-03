# tests/test_world_generation.py
"""
Script de prueba para visualizar la generación de mapas del mundo.
Permite navegar entre mapa mundial y mapas locales.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.world.map_generator import MapGenerator, Terrain


def print_menu():
    """Muestra menú de opciones."""
    print("\n" + "="*60)
    print("GENERADOR DE MAPAS DEL MUNDO - MENU")
    print("="*60)
    print("1. Ver mapa mundial (64x64 bloques de 1km)")
    print("2. Ver estadísticas del mapa mundial")
    print("3. Explorar región local (32x32 bloques de 5m)")
    print("4. Comparar alturas (mundial vs local)")
    print("5. Ver leyenda de terrenos")
    print("6. Generar nuevo mapa (diferente semilla)")
    print("0. Salir")
    print("="*60)


def print_legend():
    """Muestra leyenda de terrenos."""
    print("\nLEYENDA DE TERRENOS:")
    print("="*60)
    terrains = {
        "DEEP_OCEAN": ("🌊", "< -0.6", "Océano profundo (viaje peligroso)"),
        "OCEAN": ("🌊", "-0.6 a -0.2", "Océano normal"),
        "SHALLOW_WATER": ("💧", "-0.2 a 0.0", "Agua poco profunda (fácil cruzar)"),
        "SAND": ("🟨", "0.0 a 0.1", "Arena/Playa"),
        "GRASS": ("🟩", "0.1 a 0.3", "Pasto/Llanura"),
        "FOREST": ("🟩", "0.3 a 0.5", "Bosque (obstáculos naturales)"),
        "MOUNTAINS": ("🏔️", "0.5 a 0.7", "Montañas (movimiento lento)"),
        "SNOW_PEAKS": ("⛰️", "> 0.7", "Picos nevados (intransitable)"),
        "DEEP_CHASM": ("⬛", "< -0.8", "Grieta profunda (solo en local)"),
    }
    
    for name, (emoji, height_range, description) in terrains.items():
        print(f"{emoji} {name:15} [{height_range:12}] - {description}")
    print("="*60)


def show_world_map(generator):
    """Muestra el mapa mundial."""
    print("\nGenerando mapa mundial...")
    world_map = generator.generate_world_map(width=64, height=64)
    
    print("\nMAPO MUNDIAL (1km por bloque):")
    print("="*60)
    visualization = generator.visualize_world_map(world_map, show_coordinates=True)
    print(visualization)
    print("="*60)
    
    return world_map


def show_local_map(generator, world_x, world_y):
    """Muestra un mapa local."""
    print(f"\nGenerando mapa local para región ({world_x}, {world_y})...")
    local_map = generator.generate_local_map(world_x, world_y, local_width=32, local_height=32)
    
    print(f"\nMAPA LOCAL - REGIÓN ({world_x}, {world_y}) (5m por bloque):")
    print("="*60)
    visualization = generator.visualize_local_map(local_map, show_coordinates=True)
    print(visualization)
    print("="*60)
    
    return local_map


def show_statistics(world_map):
    """Muestra estadísticas del mapa."""
    stats = MapGenerator().get_map_statistics(world_map)
    
    print("\nESTADÍSTICAS DEL MAPA MUNDIAL:")
    print("="*60)
    print(f"Total de celdas: {stats['total_tiles']}")
    print(f"Altura promedio: {stats['average_height']:.3f}")
    print(f"Altura mínima: {stats['min_height']:.3f}")
    print(f"Altura máxima: {stats['max_height']:.3f}")
    print(f"\nDistribución de terrenos:")
    
    for terrain_name, percentage in sorted(
        stats['terrain_percentages'].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        count = stats['terrain_counts'][terrain_name]
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"  {terrain_name:15} {percentage:6.2f}% ({count:4d} celdas) {bar}")
    print("="*60)


def compare_scales(generator, world_x, world_y):
    """Compara escalas del mapa mundial y local."""
    print("\nGenerando mapas para comparación...")
    
    # Mapa mundial (solo la región seleccionada)
    world_map = generator.generate_world_map(width=10, height=10)
    
    # Mapa local
    local_map = generator.generate_local_map(world_x, world_y, local_width=32, local_height=32)
    
    print("\nCOMPARACIÓN DE ESCALAS:")
    print("="*60)
    
    print(f"\n1. MAPA MUNDIAL (región alrededor de {world_x}, {world_y}):")
    print("-"*30)
    world_viz = generator.visualize_world_map(world_map[:10, :10], show_coordinates=True)
    print(world_viz)
    
    print(f"\n2. MAPA LOCAL (región {world_x}, {world_y}) - 5 metros por bloque:")
    print("-"*30)
    local_viz = generator.visualize_local_map(local_map, show_coordinates=True)
    print(local_viz)
    
    # Comparar con altura
    print(f"\n3. MAPA LOCAL CON ALTURAS (valores de -9 a 9):")
    print("-"*30)
    local_heights = generator.visualize_local_map(local_map, show_coordinates=True, show_heights=True)
    print(local_heights)
    
    print("="*60)


def interactive_exploration(generator):
    """Permite exploración interactiva de mapas."""
    world_map = show_world_map(generator)
    
    while True:
        print("\nOpciones de exploración:")
        print("1. Ver región local")
        print("2. Ver estadísticas")
        print("3. Comparar escalas")
        print("4. Volver a menú principal")
        
        choice = input("\nElige opción (1-4): ").strip()
        
        if choice == "1":
            try:
                x = int(input("Coordenada X (0-63): "))
                y = int(input("Coordenada Y (0-63): "))
                if 0 <= x < 64 and 0 <= y < 64:
                    show_local_map(generator, x, y)
                else:
                    print("Coordenadas fuera de rango!")
            except ValueError:
                print("Entrada inválida!")
        
        elif choice == "2":
            show_statistics(world_map)
        
        elif choice == "3":
            try:
                x = int(input("Coordenada X (0-63): "))
                y = int(input("Coordenada Y (0-63): "))
                if 0 <= x < 64 and 0 <= y < 64:
                    compare_scales(generator, x, y)
                else:
                    print("Coordenadas fuera de rango!")
            except ValueError:
                print("Entrada inválida!")
        
        elif choice == "4":
            break


def main():
    """Función principal."""
    print("\n" + "="*60)
    print("SISTEMA DE GENERACIÓN DE MAPAS DEL MUNDO")
    print("="*60)
    print("Usando Perlin Noise con jerarquía de dos niveles:")
    print("  - Mapa mundial: 64x64 celdas (1km cada una)")
    print("  - Mapa local: 32x32 celdas (5m cada una)")
    print("="*60)
    
    generator = MapGenerator(seed=42)
    current_seed = 42
    
    while True:
        print_menu()
        choice = input("\nElige opción (0-6): ").strip()
        
        if choice == "1":
            world_map = show_world_map(generator)
        
        elif choice == "2":
            world_map = generator.generate_world_map(width=64, height=64)
            show_statistics(world_map)
        
        elif choice == "3":
            try:
                x = int(input("Coordenada X del mundo (0-63): "))
                y = int(input("Coordenada Y del mundo (0-63): "))
                if 0 <= x < 64 and 0 <= y < 64:
                    show_local_map(generator, x, y)
                else:
                    print("Coordenadas fuera de rango (0-63)!")
            except ValueError:
                print("Entrada inválida!")
        
        elif choice == "4":
            try:
                x = int(input("Coordenada X (0-63): "))
                y = int(input("Coordenada Y (0-63): "))
                if 0 <= x < 64 and 0 <= y < 64:
                    compare_scales(generator, x, y)
                else:
                    print("Coordenadas fuera de rango!")
            except ValueError:
                print("Entrada inválida!")
        
        elif choice == "5":
            print_legend()
        
        elif choice == "6":
            try:
                new_seed = int(input("Nueva semilla (ej: 12345): "))
                generator = MapGenerator(seed=new_seed)
                current_seed = new_seed
                print(f"Generador reinicializado con semilla {new_seed}")
                print("Los mapas serán diferentes ahora.")
            except ValueError:
                print("Semilla inválida!")
        
        elif choice == "0":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción inválida!")


if __name__ == "__main__":
    main()
