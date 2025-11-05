import os
import json
from InquirerPy import inquirer
from saves.utilities.entity import Entity
from pathlib import Path
import random
import datetime
import uuid

# Obtener la ruta base del proyecto
# === RUTAS PORTABLES ===
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # -> raíz del proyecto (E:\jogo)
DATA_DIR = BASE_DIR / "data"

RACES_PATH = DATA_DIR / "races.json"
STATS_PATH = DATA_DIR / "stats.json"

def create_player():
    # Cargar archivos JSON
    with open(RACES_PATH, "r", encoding="utf-8") as f:
        races_data = json.load(f)
    with open(STATS_PATH, "r", encoding="utf-8") as f:
        stats_data = json.load(f)

    # 1️⃣ Selección del nombre del jugador
    player_name = inquirer.text(
        message="Ingresa el nombre de tu personaje:",
        default="Jugador"
    ).execute()

    # 2️⃣ Selección de raza
    race_options = [race["display"] for race in races_data]
    choice_race = inquirer.select(
        message="Selecciona una raza:",
        choices=race_options
    ).execute()

    selected_race = next((r for r in races_data if r["display"] == choice_race), None)
    if not selected_race:
        print("❌ Error: raza no encontrada.")
        return None

    print(f"\nHas escogido la raza: {selected_race['display']}")
    print(f"Descripción: {selected_race['description']}\n")

    # 3️⃣ Inicializar estadísticas base
    stats = {stat["stat_name"]: 10 for stat in stats_data}

    # 4️⃣ Aplicar modificadores raciales
    print("Aplicando modificadores raciales:")
    for mod in selected_race["modifiers"]:
        stat_name = mod["stat_name"]
        modifier = mod["modifier"]
        if stat_name in stats:
            stats[stat_name] += modifier
            print(f"  - {stat_name.capitalize()}: +{modifier}")
        else:
            print(f"  ⚠️ Stat desconocida: {stat_name}")

    # 5️⃣ Seleccionar edad inicial
    while True:
        try:
            age_input = inquirer.text(message="Ingresa la edad inicial del personaje (en años):", default="18").execute()
            age = int(age_input)
            if age <= 0:
                raise ValueError
            break
        except ValueError:
            print("⚠️ Ingresa un número válido mayor que 0.")

    # 6️⃣ Confirmación de datos
    print("\n📋 **Resumen de tu personaje**")
    print(f"Nombre: {player_name}")
    print(f"Raza: {selected_race['display']}")
    print(f"Edad: {age} años")
    print("Estadísticas finales:")
    for key, value in stats.items():
        print(f"  - {key.capitalize()}: {value}")

    confirm = inquirer.confirm(
        message="¿Confirmar creación del personaje?",
        default=True
    ).execute()

    if not confirm:
        print("❌ Creación cancelada por el usuario.")
        return None

    # 7️⃣ Crear entidad del jugador
    player_entity = Entity(name=player_name, new_stats=stats, height=0)
    player_entity.race = {selected_race["race_name"]: 100}
    player_entity.age = age
    player_entity.height = random.randint(int(selected_race["min_height"]), int(selected_race["max_height"]))

    print("\n✅ Jugador creado con éxito.")
    print(f"👉 Nombre: {player_entity.name}")
    print(f"👉 Raza: {list(player_entity.race.keys())[0]}")
    print(f"👉 Edad: {player_entity.age}")
    print("👉 Stats iniciales:")
    for k, v in player_entity.stats.items():
        print(f"   - {k.capitalize()}: {v}")

    # 🔹 Crear carpeta de partida y guardar jugador
    save_player(player_entity)

    return player_entity


def save_player(player_entity):
    """Guarda el jugador en un archivo JSON dentro de saves/games/partida_xxxxxx/"""
    games_dir = BASE_DIR / "saves" / "games"
    os.makedirs(games_dir, exist_ok=True)

    # ID único para la partida
    game_id = f"partida_{uuid.uuid4().hex[:6]}"
    game_dir = games_dir / game_id
    os.makedirs(game_dir, exist_ok=True)

    player_save_path = game_dir / "player.json"

    player_data = {
        "meta": {
            "save_name": game_id,
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "0.1-alpha"
        },
        "player": {
            "name": player_entity.name,
            "race": player_entity.race,
            "age": player_entity.age,
            "height": player_entity.height,
            "stats": player_entity.stats,
            "level": player_entity.level,
            "experience": player_entity.experience,
            "state": player_entity.state,
            "hunger": player_entity.hunger,
            "thirst": player_entity.thirst,
            "tiredness": player_entity.tiredness,
            "reputation": player_entity.reputation
        }
    }

    with open(player_save_path, "w", encoding="utf-8") as f:
        json.dump(player_data, f, indent=4, ensure_ascii=False)

    print(f"\n💾 Partida guardada: {game_id}")
    print(f"📁 Archivo de jugador: {player_save_path}")