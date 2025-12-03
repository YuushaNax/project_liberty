#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de uso avanzado: Creación de un pueblo con NPCs variados.
Demuestra la integración completa del sistema de generación de nombres.
"""

import sys
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.entities.npc import NPC


class Town:
    """Representa un pueblo con NPCs."""
    
    def __init__(self, name, town_type="village"):
        """
        Inicializa un pueblo.
        
        Args:
            name: Nombre del pueblo
            town_type: Tipo de pueblo (village, town, city)
        """
        self.name = name
        self.town_type = town_type
        self.npcs = {}
        self.npc_locations = {}
    
    def add_npc(self, location, profession, race="human", npc_name=None):
        """
        Agrega un NPC al pueblo.
        
        Args:
            location: Ubicación en el pueblo (ej: "tavern", "forge", "market")
            profession: Profesión del NPC
            race: Raza del NPC
            npc_name: Nombre específico (opcional)
        
        Returns:
            El NPC creado
        """
        try:
            npc = NPC(
                name=npc_name,
                profession_name=profession,
                race_name=race,
                auto_generate_name=npc_name is None
            )
            
            if location not in self.npc_locations:
                self.npc_locations[location] = []
            
            self.npc_locations[location].append(npc)
            self.npcs[npc.name] = npc
            
            return npc
        except Exception as e:
            print(f"Error creando NPC: {e}")
            return None
    
    def populate_randomly(self, population_size=20):
        """
        Puebla el pueblo con NPCs aleatorios.
        
        Args:
            population_size: Cantidad de NPCs a crear
        """
        locations = ["tavern", "market", "forge", "shop", "farm", "house", "temple", "inn"]
        civilian_professions = [
            "tailor", "baker", "blacksmith", "carpenter", "innkeeper",
            "farmer", "scholar", "healer", "merchant", "cook", "scribe",
            "fisherman", "miner", "alchemist", "priest", "jeweler"
        ]
        combat_professions = [
            "warrior", "rogue", "archer", "mage", "paladin", "cleric"
        ]
        races = ["human", "elf", "dwarf", "halfling", "orc", "tiefling"]
        
        for i in range(population_size):
            # 80% civiles, 20% combatientes
            if random.random() < 0.8:
                profession = random.choice(civilian_professions)
            else:
                profession = random.choice(combat_professions)
            
            location = random.choice(locations)
            race = random.choice(races)
            
            self.add_npc(location, profession, race)
    
    def display_town_info(self):
        """Muestra información del pueblo."""
        print("=" * 80)
        print(f"PUEBLO: {self.name.upper()} ({self.town_type})")
        print("=" * 80)
        print(f"Total de NPCs: {len(self.npcs)}\n")
    
    def display_by_location(self):
        """Muestra los NPCs agrupados por ubicación."""
        print("\n[NPCS POR UBICACION]\n")
        
        for location in sorted(self.npc_locations.keys()):
            npcs_in_location = self.npc_locations[location]
            print(f"{location.upper()}:")
            
            for npc in npcs_in_location:
                race_name = list(npc.race.keys())[0]
                
                print(f"  {npc.get_full_title()}")
                print(f"     - Stats: STR={npc.stats['strength']}, DEX={npc.stats['dexterity']}, CON={npc.stats['constitution']}")
                print(f"     - Comportamiento: {npc.get_npc_values_summary()}")
                print()
    
    def display_by_profession(self):
        """Muestra los NPCs agrupados por profesión."""
        print("\n[NPCS POR PROFESION]\n")
        
        # Agrupar por profesión
        by_profession = {}
        for npc in self.npcs.values():
            prof = npc.profession_display
            if prof not in by_profession:
                by_profession[prof] = []
            by_profession[prof].append(npc)
        
        for profession in sorted(by_profession.keys()):
            npcs_with_profession = by_profession[profession]
            print(f"{profession.upper()} ({len(npcs_with_profession)}):")
            
            for npc in npcs_with_profession:
                race_name = list(npc.race.keys())[0]
                print(f"  * {npc.name:15} - {race_name:10} - Agresividad: {npc.npc_values['aggressiveness']:3}/100")
            print()
    
    def create_scenario(self):
        """Crea un escenario de diálogo entre NPCs."""
        print("\n[ESCENARIO DE DIALOGO]\n")
        print("=" * 80)
        
        if len(self.npcs) < 2:
            print("No hay suficientes NPCs para crear un dialogo.")
            return
        
        # Seleccionar NPCs aleatorios
        npc_list = list(self.npcs.values())
        npc1 = random.choice(npc_list)
        npc2 = random.choice([n for n in npc_list if n != npc1])
        npc3 = random.choice([n for n in npc_list if n != npc1 and n != npc2])
        
        location = list(self.npc_locations.keys())[0]
        
        print(f"[LOCACION: {location.upper()}]\n")
        
        print(f"{npc1.get_full_title(include_race=True)} entra en la taberna.\n")
        
        print(f"{npc1.get_reference_by_profession()}:")
        print(f'  "!Hola! Como estan ustedes por aqui?"\n')
        
        print(f"{npc2.get_reference_by_profession()}:")
        print(f'  "!Bien, bien! Hace poco llego {npc3.get_reference_by_profession()}')
        print(f'   nos ha contado historias fascinantes."')
        print(f'  Agresividad del {npc3.profession_display}: {npc3.npc_values["aggressiveness"]}/100\n')
        
        print(f"{npc3.get_reference_by_profession()}:")
        if npc3.would_initiate_combat():
            print(f'  "!Bah! Deja de hablar tonterias y preparate para la batalla"')
            print(f'  (Iniciara combate)')
        else:
            print(f'  "Jaja, no es para tanto. Solo compartiendo mis aventuras."')
            print(f'  (No iniciara combate)')
        print()


def example_1_simple_town():
    """Ejemplo 1: Crear un pueblo simple."""
    print("\n" + "=" * 80)
    print("EJEMPLO 1: PUEBLO SIMPLE")
    print("=" * 80 + "\n")
    
    town = Town("Millhaven", town_type="village")
    
    # Agregar NPCs manualmente
    town.add_npc("tavern", "innkeeper", "human", "Garrick")
    town.add_npc("tavern", "bard", "human")
    town.add_npc("forge", "blacksmith", "dwarf")
    town.add_npc("market", "merchant", "human")
    town.add_npc("temple", "priest", "human")
    
    town.display_town_info()
    town.display_by_location()


def example_2_random_population():
    """Ejemplo 2: Puebla un pueblo de forma aleatoria."""
    print("\n" + "=" * 80)
    print("EJEMPLO 2: PUEBLO ALEATORIO CON 25 NPCs")
    print("=" * 80 + "\n")
    
    town = Town("Aethermoor", town_type="city")
    town.populate_randomly(25)
    
    town.display_town_info()
    town.display_by_profession()


def example_3_dialogue_scenario():
    """Ejemplo 3: Crear un escenario de diálogo."""
    print("\n" + "=" * 80)
    print("EJEMPLO 3: ESCENARIOS DE DIÁLOGO")
    print("=" * 80 + "\n")
    
    town = Town("Thornwick", town_type="town")
    town.populate_randomly(10)
    
    # Crear varios escenarios
    for i in range(3):
        town.create_scenario()
        print("=" * 80 + "\n")


def example_4_advanced_statistics():
    """Ejemplo 4: Estadísticas avanzadas del pueblo."""
    print("\n" + "=" * 80)
    print("EJEMPLO 4: ESTADISTICAS DEL PUEBLO")
    print("=" * 80 + "\n")
    
    town = Town("Valdris", town_type="city")
    town.populate_randomly(50)
    
    # Análisis de stats
    print("[ANALISIS DE POBLACION]\n")
    
    avg_aggression = sum(npc.npc_values["aggressiveness"] for npc in town.npcs.values()) / len(town.npcs)
    avg_honesty = sum(npc.npc_values["honesty"] for npc in town.npcs.values()) / len(town.npcs)
    avg_loyalty = sum(npc.npc_values["loyalty"] for npc in town.npcs.values()) / len(town.npcs)
    
    print(f"Total de NPCs: {len(town.npcs)}")
    print(f"Agresividad promedio: {avg_aggression:.1f}/100")
    print(f"Honestidad promedio: {avg_honesty:.1f}/100")
    print(f"Lealtad promedio: {avg_loyalty:.1f}/100")
    
    # Razas
    races = {}
    for npc in town.npcs.values():
        race = list(npc.race.keys())[0]
        races[race] = races.get(race, 0) + 1
    
    print(f"\n[RAZAS]")
    for race, count in sorted(races.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(town.npcs)) * 100
        print(f"  {race:10} - {count:2} NPCs ({percentage:5.1f}%)")
    
    # Profesiones más comunes
    professions = {}
    for npc in town.npcs.values():
        prof = npc.profession_display
        professions[prof] = professions.get(prof, 0) + 1
    
    print(f"\n[PROFESIONES MAS COMUNES]")
    top_professions = sorted(professions.items(), key=lambda x: x[1], reverse=True)[:5]
    for profession, count in top_professions:
        print(f"  {profession:15} - {count:2} NPCs")
    
    # Potencial de combate
    combat_ready = sum(1 for npc in town.npcs.values() if npc.npc_values["aggressiveness"] > 70)
    print(f"\n[POTENCIAL DE COMBATE] (>70% agresividad): {combat_ready}")
    
    # Potencial de traición
    traitors = sum(1 for npc in town.npcs.values() if npc.npc_values["loyalty"] < 30)
    print(f"[POTENCIAL DE TRAICION] (<30% lealtad): {traitors}")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("EJEMPLOS DE USO AVANZADO: CREACION DE PUEBLOS CON NPCs")
    print("=" * 80)
    
    try:
        # Ejecutar ejemplos
        example_1_simple_town()
        example_2_random_population()
        example_3_dialogue_scenario()
        example_4_advanced_statistics()
        
        print("\n" + "=" * 80)
        print("OK - TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
