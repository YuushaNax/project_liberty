#player.py

import os
import json
from InquirerPy import inquirer
from entity import Entity

races_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '././data/races.json')
stats_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '././data/stats.json')

options = []
with open(races_path, 'r', encoding='utf-8') as f:
    races_data = json.load(f)
with open(stats_path, 'r', encoding='utf-8') as f:
    stats_data = json.load(f)

for race in races_data:
    options.append(race['display'])

choice_race = inquirer.select(
    message="Selecciona una raza:",
    choices=options
).execute()

for race in races_data:
    if race['display'] == choice_race:
        print("ESCOGISTE: ", race['display'])
        print("Descripción: ", race['description'])
        print("Modificadores: ")
        for mod in race['modifiers']:
            stat=mod['stat_name']
            for stat_existent in stats_data:
                if stat_existent['stat_name'] == stat:
                    stat=stat_existent['display']
            value=mod['modifier']
            print(f" - {stat.capitalize()}: {value}")
    
