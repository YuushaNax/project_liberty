#!/usr/bin/env python3
"""
Script para generar 100 personajes y analizar:
1. Eventos más comunes
2. Detección de personajes exactamente iguales
"""

import json
import random
from pathlib import Path
from collections import Counter, defaultdict
from engine.entities.entity import Entity

BASE_DIR = Path(__file__).resolve().parent
DATA = BASE_DIR / "data"
GAMES = BASE_DIR / "saves" / "games"

# Cargar datos
with open(DATA / "races.json", encoding="utf-8") as f:
    races_data = json.load(f)

with open(DATA / "stats.json", encoding="utf-8") as f:
    stats_data = json.load(f)

with open(DATA / "childhood_events.json", encoding="utf-8") as f:
    childhood_data = json.load(f)


def generate_character():
    """Genera un personaje único con su journey de infancia."""
    # Seleccionar raza
    selected_race = random.choice(races_data)
    maturity_age = int(selected_race.get("maturity", 18))
    
    # Inicializar stats
    stats = {s["stat_name"]: 10 for s in stats_data}
    
    # Aplicar modificadores de raza
    for mod in selected_race.get("modifiers", []):
        stat_name = mod.get("stat_name")
        modifier = mod.get("modifier", 0)
        if stat_name in stats:
            try:
                stats[stat_name] += int(modifier)
            except Exception:
                stats[stat_name] += float(modifier)
    
    # Generar journey de infancia
    childhood_history = []
    age = 0
    age_progression_index = 0
    
    age_categories = [
        (0, "birth"),
        (1, "age_1_2"),
        (3, "age_3_5"),
        (6, "age_6_10"),
        (11, "age_11_15"),
        (16, "age_16_20"),
    ]
    
    while age < maturity_age:
        # Encontrar la categoría actual
        current_category = None
        for threshold_age, category_name in age_categories:
            if age >= threshold_age:
                current_category = category_name
        
        # Cargar eventos disponibles
        events = childhood_data.get(current_category, [])
        
        # Filtrar por rareness
        available_events = []
        for event in events:
            rareness = event.get("rareness", 0.5)
            if random.random() < rareness:
                available_events.append(event)
        
        # Si no hay eventos en la categoría, agregar special events
        if not available_events and current_category:
            special_events = childhood_data.get("special_events", [])
            for event in special_events:
                rareness = event.get("rareness", 0.5)
                if random.random() < rareness:
                    available_events.append(event)
        
        # Si aún no hay eventos, crear uno aleatorio de la categoría
        if not available_events and events:
            available_events = [random.choice(events)]
        
        if not available_events:
            break
        
        # Seleccionar evento y opción
        selected_event = random.choice(available_events)
        opts = selected_event.get("options", [])
        
        if opts:
            selected_option = random.choice(opts)
        else:
            selected_option = None
        
        # Aplicar efectos
        if selected_option:
            effects = selected_option.get("effect", {})
            for stat_name, delta in effects.items():
                if stat_name in stats:
                    try:
                        stats[stat_name] += int(delta)
                    except Exception:
                        stats[stat_name] += float(delta)
            
            childhood_history.append({
                "age": age,
                "event_name": selected_event.get("event_name"),
                "option_name": selected_option.get("option_name"),
                "effects": effects
            })
        
        age += 1
    
    # Crear entidad
    min_h = int(selected_race.get("min_height", 150))
    max_h = int(selected_race.get("max_height", 200))
    # Asegurar que min_h <= max_h
    if min_h > max_h:
        min_h, max_h = max_h, min_h
    
    player = Entity(
        name=f"Char_{random.randint(1000, 9999)}",
        new_stats=stats,
        height=random.randint(min_h, max_h),
    )
    player.race = {selected_race.get("race_name", selected_race.get("display")): 100}
    player.age = age
    
    return {
        "name": player.name,
        "race": player.race,
        "age": player.age,
        "stats": player.stats,
        "height": player.height,
        "childhood_journey": childhood_history,
    }


def main():
    # Número de personajes a generar (puede modificarse)
    NUM_CHARACTERS = 100000000
    
    print("=" * 80)
    print(f"GENERANDO {NUM_CHARACTERS} PERSONAJES Y ANALIZANDO MÉTRICAS")
    print("=" * 80)
    print()
    
    characters = []
    event_counter = Counter()
    option_counter = Counter()
    journey_hashes = defaultdict(int)
    
    print(f"Generando {NUM_CHARACTERS} personajes...")
    for i in range(NUM_CHARACTERS):
        char = generate_character()
        characters.append(char)
        
        # Contar eventos
        for journey_item in char["childhood_journey"]:
            event_name = journey_item.get("event_name")
            option_name = journey_item.get("option_name")
            
            event_counter[event_name] += 1
            if option_name:
                option_counter[option_name] += 1
        
        # Hash para detectar duplicados
        journey_tuple = tuple(
            (item["event_name"], item["option_name"]) for item in char["childhood_journey"]
        )
        journey_hashes[journey_tuple] += 1
        
        if (i + 1) % (NUM_CHARACTERS // 4) == 0:
            print(f"  Generados {i + 1}/{NUM_CHARACTERS} personajes...")
    
    print(f"✓ Generación completada.\n")
    
    # ==========================================
    # ANÁLISIS 1: EVENTOS MÁS COMUNES
    # ==========================================
    print("=" * 80)
    print("ANÁLISIS 1: EVENTOS MÁS COMUNES")
    print("=" * 80)
    print()
    
    print(f"Total de eventos únicos: {len(event_counter)}")
    print(f"Total de ocurrencias de eventos: {sum(event_counter.values())}\n")
    
    print("TOP 20 EVENTOS MÁS FRECUENTES:")
    print("-" * 80)
    print(f"{'Rango':<6} {'Evento':<40} {'Frecuencia':<12} {'%':<8}")
    print("-" * 80)
    
    for rank, (event_name, count) in enumerate(event_counter.most_common(20), 1):
        percentage = (count / sum(event_counter.values())) * 100
        print(f"{rank:<6} {event_name:<40} {count:<12} {percentage:>6.1f}%")
    
    print()
    print("BOTTOM 10 EVENTOS MENOS FRECUENTES:")
    print("-" * 80)
    print(f"{'Evento':<40} {'Frecuencia':<12}")
    print("-" * 80)
    
    for event_name, count in event_counter.most_common()[-10:]:
        print(f"{event_name:<40} {count:<12}")
    
    print()
    
    # ==========================================
    # ANÁLISIS 2: OPCIONES MÁS COMUNES
    # ==========================================
    print("=" * 80)
    print("ANÁLISIS 2: OPCIONES MÁS COMUNES")
    print("=" * 80)
    print()
    
    print(f"Total de opciones únicas: {len(option_counter)}")
    print(f"Total de ocurrencias de opciones: {sum(option_counter.values())}\n")
    
    print("TOP 15 OPCIONES MÁS ELEGIDAS:")
    print("-" * 80)
    print(f"{'Rango':<6} {'Opción':<45} {'Frecuencia':<12}")
    print("-" * 80)
    
    for rank, (option_name, count) in enumerate(option_counter.most_common(15), 1):
        print(f"{rank:<6} {option_name:<45} {count:<12}")
    
    print()
    
    # ==========================================
    # ANÁLISIS 3: DETECCIÓN DE DUPLICADOS
    # ==========================================
    print("=" * 80)
    print("ANÁLISIS 3: DETECCIÓN DE PERSONAJES DUPLICADOS")
    print("=" * 80)
    print()
    
    duplicates = {journey: count for journey, count in journey_hashes.items() if count > 1}
    
    if duplicates:
        print(f"⚠️  DUPLICADOS ENCONTRADOS: {len(duplicates)} journeys diferentes repetidas\n")
        
        sorted_dups = sorted(duplicates.items(), key=lambda x: x[1], reverse=True)
        
        for idx, (journey_tuple, count) in enumerate(sorted_dups, 1):
            print(f"\nDuplicado #{idx}: Repetido {count} veces")
            print(f"  Journey (eventos + opciones seleccionadas):")
            
            for step_idx, (event, option) in enumerate(journey_tuple, 1):
                print(f"    Paso {step_idx}: {event} → {option}")
    else:
        print("✓ No hay personajes exactamente iguales en los 100 generados.")
        print("  Cada journey de infancia fue único.")
    
    print()
    print(f"Total de journeys únicos: {len(journey_hashes)} / {NUM_CHARACTERS}")
    print(f"Tasa de diversidad: {(len(journey_hashes) / NUM_CHARACTERS) * 100:.1f}%")
    
    print()
    print("=" * 80)
    print("FIN DEL ANÁLISIS")
    print("=" * 80)


if __name__ == "__main__":
    main()
