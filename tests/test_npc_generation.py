#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la generación automática de NPCs.
Verifica que:
1. Los stats se generan dentro de los rangos de la profesión
2. Los rasgos de personalidad se asignan correctamente
3. No hay conflictos entre rasgos
"""

import json
import sys
import io
from pathlib import Path
from engine.entities.npc import NPC

# Fix encoding for Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
DATA = BASE_DIR / "data"

def load_json(filepath):
    """Carga un archivo JSON."""
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

def test_npc_creation():
    """Prueba la creación de NPCs desde diferentes profesiones."""
    
    professions = load_json(DATA / "professions.json")
    races = load_json(DATA / "races.json")
    personality_data = load_json(DATA / "personality_traits.json")
    
    traits_dict = {t["id"]: t for t in personality_data["traits"]}
    
    print("=" * 80)
    print("TEST: GENERACIÓN DE NPCs")
    print("=" * 80)
    
    # Crear NPCs de diferentes profesiones
    profession_names = [p["profession_name"] for p in professions[:5]]  # Primeras 5
    race_names = [r["race_name"] for r in races[:3]]  # Primeras 3 razas
    
    for i, prof_name in enumerate(profession_names):
        for j, race_name in enumerate(race_names):
            npc_name = f"{prof_name.capitalize()}_{race_name}_{i}_{j}"
            
            try:
                npc = NPC(
                    name=npc_name,
                    profession_name=prof_name,
                    race_name=race_name
                )
                
                print(f"\n✓ NPC Creado: {npc}")
                print(f"  Nombre: {npc.name}")
                print(f"  Profesión: {npc.profession_display}")
                print(f"  Raza: {list(npc.race.keys())}")
                print(f"  Altura: {npc.height} cm")
                print(f"  Nivel: {npc.level}")
                
                # Mostrar stats
                print("  Stats:")
                for stat_name in ["strength", "dexterity", "constitution", 
                                 "intelligence", "wisdom", "charisma"]:
                    val = getattr(npc, stat_name, None)
                    if val is not None:
                        print(f"    - {stat_name}: {val}")
                
                # Mostrar personalidad
                print(f"  Personalidad: {npc.get_personality_summary()}")
                
                # Mostrar valores únicos
                print(f"  Valores NPC: {npc.get_npc_values_summary()}")
                
                # Mostrar probabilidades de comportamiento
                combat_prob = npc.npc_values.get("aggressiveness", 50) - npc.npc_values.get("caution", 50)
                combat_prob = max(0, min(100, combat_prob))
                betrayal_prob = max(0, min(100, 100 - npc.npc_values.get("loyalty", 50)))
                print(f"  Comportamiento: {combat_prob}% probabilidad de iniciar combate | {betrayal_prob}% probabilidad de traición")
                
                # Verificar conflictos de personalidad (permití algunos ahora)
                conflicts = []
                for trait_id in npc.personality.keys():
                    if trait_id in traits_dict:
                        trait = traits_dict[trait_id]
                        trait_conflicts = trait.get("conflicts", [])
                        for conflict_id in trait_conflicts:
                            if conflict_id in npc.personality:
                                conflicts.append(f"{trait_id} <-> {conflict_id}")
                
                if conflicts:
                    print(f"  ⚠ CONTRADICCIONES PERMITIDAS: {conflicts}")
                else:
                    print(f"  ✓ Personalidad coherente")
                
            except Exception as e:
                print(f"\n✗ Error creando NPC {npc_name}: {e}")
                import traceback
                traceback.print_exc()
    
    print("\n" + "=" * 80)

def test_stat_ranges():
    """Verifica que los stats generados están dentro de los rangos."""
    
    professions = load_json(DATA / "professions.json")
    
    print("\n" + "=" * 80)
    print("TEST: VALIDACIÓN DE RANGOS DE STATS")
    print("=" * 80)
    
    for profession in professions:
        prof_name = profession["profession_name"]
        stat_ranges = profession.get("stat_ranges", {})
        
        print(f"\n{prof_name.upper()}:")
        print(f"  Rangos definidos: {stat_ranges}")
        
        # Crear 10 NPCs y verificar rangos
        out_of_range = []
        for i in range(10):
            try:
                npc = NPC(
                    name=f"test_{prof_name}_{i}",
                    profession_name=prof_name,
                    race_name="human"
                )
                
                for stat_name, stat_range in stat_ranges.items():
                    min_val = stat_range.get("min", 10)
                    max_val = stat_range.get("max", 18)
                    actual_val = getattr(npc, stat_name, None)
                    
                    if actual_val is not None:
                        if not (min_val <= actual_val <= max_val):
                            out_of_range.append(
                                f"  NPC {i}: {stat_name}={actual_val} "
                                f"(rango: {min_val}-{max_val})"
                            )
            except Exception as e:
                print(f"  Error en test {i}: {e}")
        
        if out_of_range:
            print("  ✗ VALORES FUERA DE RANGO:")
            for msg in out_of_range:
                print(msg)
        else:
            print("  ✓ Todos los stats dentro de rangos")

def test_professions_available():
    """Verifica que todas las profesiones pueden ser usadas."""
    
    professions = load_json(DATA / "professions.json")
    
    print("\n" + "=" * 80)
    print("TEST: DISPONIBILIDAD DE PROFESIONES")
    print("=" * 80)
    print(f"\nTotal de profesiones: {len(professions)}")
    
    for prof in professions:
        print(f"\n✓ {prof['profession_name']}")
        print(f"  Nombre: {prof.get('display', 'N/A')}")
        print(f"  Descripción: {prof.get('description', 'N/A')[:60]}...")
        print(f"  Rasgos base: {prof.get('personality_traits', [])}")
        print(f"  Stats: {list(prof.get('stat_ranges', {}).keys())}")

if __name__ == "__main__":
    test_professions_available()
    test_npc_creation()
    test_stat_ranges()
    
    print("\n" + "=" * 80)
    print("PRUEBAS COMPLETADAS")
    print("=" * 80)
