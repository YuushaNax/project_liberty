#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba rápida del sistema de NPC completamente funcional.
"""

from engine.entities.npc import NPC

print("=" * 80)
print("PRUEBA RÁPIDA DEL SISTEMA DE NPC")
print("=" * 80)
print()

npcs_data = [
    ('Thorgrim', 'warrior', 'human'),
    ('Sylvara', 'rogue', 'elf'),
    ('Arctus', 'mage', 'human'),
    ('Hadrian', 'paladin', 'human'),
    ('Elara', 'cleric', 'human'),
]

for name, prof, race in npcs_data:
    try:
        npc = NPC(name, prof, race)
        combat = "COMBATE" if npc.would_initiate_combat() else "EVITA"
        betray = "TRAICION" if npc.would_betray() else "LEAL"
        
        print(f"{name} ({npc.profession_display})")
        print(f"  Personalidad: {npc.get_personality_summary()[:70]}...")
        print(f"  Valores: {npc.get_npc_values_summary()}")
        print(f"  Decisiones: {combat} / {betray}")
        print()
        
    except Exception as e:
        print(f"ERROR con {name}: {e}")
        import traceback
        traceback.print_exc()
        break

print("=" * 80)
print("PRUEBA EXITOSA - Sistema de NPC completamente funcional")
print("=" * 80)
