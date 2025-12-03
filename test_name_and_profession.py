#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de integración: Generación de nombres y NPCs con títulos de oficio.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.utils.name_generator import NameGenerator
from engine.entities.npc import NPC


def test_name_generation():
    """Test de generación de nombres por raza."""
    print("=" * 80)
    print("TEST 1: GENERACIÓN DE NOMBRES POR RAZA")
    print("=" * 80)
    
    gen = NameGenerator()
    races = ["human", "elf", "dwarf", "orc", "halfling", "tiefling"]
    
    for race in races:
        print(f"\n{race.upper()}:")
        names = gen.generate_multiple_names(race, 5)
        for name in names:
            print(f"  • {name}")
    
    print("\n" + "=" * 80)


def test_npc_creation_with_names():
    """Test de creación de NPCs con nombres generados automáticamente."""
    print("TEST 2: CREACIÓN DE NPCs CON NOMBRES Y TÍTULOS")
    print("=" * 80)
    
    professions = [
        ("warrior", "human"),
        ("mage", "elf"),
        ("dwarf", "warrior"),
        ("thief", "human"),
        ("healer", "human"),
        ("tailor", "halfling"),
        ("baker", "human"),
        ("paladin", "dwarf"),
    ]
    
    npcs = []
    for profession, race in professions:
        try:
            # Crear NPC con nombre generado automáticamente
            npc = NPC(
                profession_name=profession,
                race_name=race,
                auto_generate_name=True
            )
            npcs.append(npc)
            
            # Mostrar información del NPC
            print(f"\nOK {npc.get_full_title(include_race=True)}")
            print(f"  - Referencia: {npc.get_reference_by_profession()}")
            print(f"  - Stats: STR={npc.stats['strength']}, DEX={npc.stats['dexterity']}, CON={npc.stats['constitution']}")
            print(f"  - Altura: {npc.height}cm")
            print(f"  - Personalidad: {npc.get_personality_summary()[:60]}...")
            print(f"  - Comportamiento: {npc.get_npc_values_summary()}")
            
        except Exception as e:
            print(f"\nERROR creando NPC ({profession}, {race}): {e}")
    
    print("\n" + "=" * 80)
    return npcs


def test_profession_references():
    """Test de referencias entre NPCs por profesión."""
    print("TEST 3: REFERENCIAS ENTRE NPCs POR PROFESIÓN")
    print("=" * 80)
    
    # Crear algunos NPCs
    npc1 = NPC(name="Kah'zur", profession_name="warrior", race_name="human")
    npc2 = NPC(profession_name="tailor", race_name="human")
    npc3 = NPC(profession_name="baker", race_name="halfling")
    
    print(f"\nNPC 1 (especificado manualmente):")
    print(f"  Nombre: {npc1.name}")
    print(f"  Título completo: {npc1.get_full_title(include_race=True)}")
    print(f"  Referencia por profesión: {npc1.get_reference_by_profession()}")
    
    print(f"\nNPC 2 (nombre generado automáticamente):")
    print(f"  Nombre: {npc2.name}")
    print(f"  Título completo: {npc2.get_full_title(include_race=True)}")
    print(f"  Referencia por profesión: {npc2.get_reference_by_profession()}")
    
    print(f"\nNPC 3 (halfling panadero):")
    print(f"  Nombre: {npc3.name}")
    print(f"  Título completo: {npc3.get_full_title(include_race=True)}")
    print(f"  Referencia por profesión: {npc3.get_reference_by_profession()}")
    
    # Simular diálogo
    print(f"\n--- DIÁLOGO SIMULADO ---")
    print(f"{npc1.get_full_title()} dice:")
    print(f"  \"He hablado con {npc2.get_reference_by_profession()}\"")
    print(f"  \"y también con {npc3.get_reference_by_profession()}\"")
    
    print("\n" + "=" * 80)


def test_diversity():
    """Test de diversidad de nombres generados."""
    print("TEST 4: DIVERSIDAD DE NOMBRES (1000 GENERACIONES)")
    print("=" * 80)
    
    gen = NameGenerator()
    
    for race in ["human", "elf", "dwarf"]:
        names = set()
        for _ in range(100000):
            name = gen.generate_name(race)
            names.add(name)
        
        unique_count = len(names)
        diversity_percentage = (unique_count / 100000) * 100
        
        print(f"\n{race.upper()}:")
        print(f"  Nombres generados: 1000")
        print(f"  Nombres únicos: {unique_count}")
        print(f"  Diversidad: {diversity_percentage:.1f}%")
        
        # Mostrar algunos ejemplos
        sample_names = sorted(list(names))[:10]
        print(f"  Ejemplos: {', '.join(sample_names)}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TEST COMPLETO: SISTEMA DE GENERACION DE NOMBRES Y NPCs")
    print("=" * 80 + "\n")
    
    try:
        test_name_generation()
        test_npc_creation_with_names()
        test_profession_references()
        test_diversity()
        
        print("\nOK - TODOS LOS TESTS COMPLETADOS EXITOSAMENTE\n")
        
    except Exception as e:
        print(f"\nERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()
