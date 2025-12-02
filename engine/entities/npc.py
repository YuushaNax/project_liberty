# engine/entities/npc.py
import json
import random
from pathlib import Path
from engine.entities.entity import Entity

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA = BASE_DIR / "data"


class NPC(Entity):
    """
    Clase para representar a un NPC (personaje no jugador) en el juego.
    Hereda de Entity y se genera automáticamente basada en una profesión.
    Los stats se generan dentro de los rangos definidos por la profesión.
    Los rasgos de personalidad se asignan según la profesión y sus sinergia.
    """

    def __init__(self, name, profession_name, race_name="human", height=None):
        """
        Inicializa un NPC basado en una profesión.
        
        Args:
            name: Nombre del NPC
            profession_name: Nombre de la profesión (ej: "warrior", "mage")
            race_name: Nombre de la raza (default: "human")
            height: Altura (opcional, se genera aleatoriamente si no se proporciona)
        """
        # Cargar datos
        with open(DATA / "professions.json", encoding="utf-8") as f:
            professions = json.load(f)
        
        with open(DATA / "races.json", encoding="utf-8") as f:
            races = json.load(f)
        
        with open(DATA / "stats.json", encoding="utf-8") as f:
            stats_data = json.load(f)
        
        with open(DATA / "personality_traits.json", encoding="utf-8") as f:
            personality_data = json.load(f)
        
        # Encontrar profesión
        profession = next(
            (p for p in professions if p["profession_name"] == profession_name),
            None
        )
        if not profession:
            raise ValueError(f"Profesión '{profession_name}' no encontrada")
        
        # Encontrar raza
        race = next(
            (r for r in races if r["race_name"] == race_name),
            None
        )
        if not race:
            raise ValueError(f"Raza '{race_name}' no encontrada")
        
        # Generar stats dentro de los rangos de la profesión
        stats = self._generate_profession_stats(profession, stats_data)
        
        # Aplicar modificadores de raza
        for mod in race.get("modifiers", []):
            stat_name = mod.get("stat_name")
            modifier = mod.get("modifier", 0)
            if stat_name in stats:
                try:
                    stats[stat_name] += int(modifier)
                except Exception:
                    stats[stat_name] += float(modifier)
        
        # Generar altura si no se proporciona
        if height is None:
            min_h = int(race.get("min_height", 150))
            max_h = int(race.get("max_height", 200))
            if min_h > max_h:
                min_h, max_h = max_h, min_h
            height = random.randint(min_h, max_h)
        
        # Inicializar Entity con los stats generados
        super().__init__(
            name=name,
            new_stats=stats,
            height=height
        )
        
        # Asignar raza
        self.race = {race.get("race_name"): 100}
        
        # Asignar profesión
        self.profession = profession_name
        self.profession_display = profession.get("display", profession_name)
        self.profession_description = profession.get("description", "")
        
        # Asignar habilidades
        self.primary_skills = profession.get("primary_skills", [])
        self.secondary_skills = profession.get("secondary_skills", [])
        
        # Generar personalidad
        self.personality = self._generate_personality(
            profession.get("personality_traits", []),
            personality_data
        )
        
        # Generar valores únicos de NPC (para comportamiento emergente)
        self.npc_values = self._generate_npc_values(
            profession_name,
            self.personality,
            personality_data
        )
    
    def _generate_profession_stats(self, profession, stats_data):
        """
        Genera stats basados en los rangos definidos por la profesión.
        Los stats se generan aleatoriamente dentro del rango [min, max].
        
        Args:
            profession: Diccionario de profesión
            stats_data: Lista de datos de stats disponibles
        
        Returns:
            Diccionario de stats generados
        """
        stats = {}
        stat_ranges = profession.get("stat_ranges", {})
        
        # Generar cada stat dentro de su rango de profesión
        for stat_info in stats_data:
            stat_name = stat_info.get("stat_name")
            
            if stat_name in stat_ranges:
                # Usar el rango de la profesión
                stat_range = stat_ranges[stat_name]
                min_val = stat_range.get("min", 10)
                max_val = stat_range.get("max", 18)
                stats[stat_name] = random.randint(min_val, max_val)
            else:
                # Stat no definido en profesión, usar valor por defecto
                stats[stat_name] = 10
        
        return stats
    
    def _generate_personality(self, profession_traits, personality_data):
        """
        Asigna rasgos de personalidad basados en la profesión.
        Permite contradicciones leves (10% de probabilidad) para más variedad y realismo.
        
        Args:
            profession_traits: Lista de trait IDs recomendados para la profesión
            personality_data: Diccionario con todos los rasgos disponibles
        
        Returns:
            Diccionario de personalidad con intensidades
        """
        traits_dict = {t["id"]: t for t in personality_data["traits"]}
        
        selected_traits = {}
        
        def _would_create_contradiction(trait_id, current_traits):
            """
            Verifica si un rasgo entraría en conflicto con los actuales.
            Retorna True si habría conflicto, False si es seguro añadirlo.
            """
            if trait_id not in traits_dict:
                return False
            
            trait = traits_dict[trait_id]
            conflicts = trait.get("conflicts", [])
            
            for conflict_id in conflicts:
                if conflict_id in current_traits:
                    return True
            return False
        
        # Agregar rasgos base de la profesión
        for trait_id in profession_traits:
            if trait_id in traits_dict:
                trait = traits_dict[trait_id]
                # Generar intensidad aleatoria dentro del rango permitido
                intensity_range = trait.get("intensity", {})
                min_intensity = intensity_range.get("min", 0)
                max_intensity = intensity_range.get("max", 100)
                intensity = random.randint(min_intensity, max_intensity)
                selected_traits[trait_id] = intensity
        
        # Intentar agregar rasgos sinérgicos (30% de probabilidad por sinergía)
        # Pero permitir algunas contradicciones leves (10% de probabilidad)
        added_synergies = set()
        for trait_id in list(selected_traits.keys()):
            if trait_id in traits_dict:
                trait = traits_dict[trait_id]
                synergies = trait.get("synergies", [])
                
                for synergy_id in synergies:
                    if (synergy_id not in selected_traits and 
                        synergy_id not in added_synergies and 
                        random.random() < 0.3):  # 30% de probabilidad
                        
                        if synergy_id in traits_dict:
                            synergy_trait = traits_dict[synergy_id]
                            
                            # Verificar conflictos pero permitir 10% de probabilidad
                            if _would_create_contradiction(synergy_id, selected_traits):
                                if random.random() > 0.10:  # Solo 10% de contradicciones
                                    continue
                            
                            intensity_range = synergy_trait.get("intensity", {})
                            min_intensity = intensity_range.get("min", 0)
                            max_intensity = intensity_range.get("max", 100)
                            intensity = random.randint(min_intensity, max_intensity)
                            selected_traits[synergy_id] = intensity
                            added_synergies.add(synergy_id)
        
        return selected_traits
    
    def _generate_npc_values(self, profession_name, personality, personality_data):
        """
        Genera valores únicos del NPC que afectan su comportamiento.
        Estos valores se derivan de la profesión y personalidad.
        
        Args:
            profession_name: Nombre de la profesión
            personality: Diccionario de personalidad del NPC
            personality_data: Datos de personalidad
        
        Returns:
            Diccionario con valores únicos del NPC
        """
        traits_dict = {t["id"]: t for t in personality_data["traits"]}
        
        # Valores base según profesión
        profession_values = {
            "warrior": {"aggressiveness": 75, "honesty": 65, "loyalty": 70, "caution": 30},
            "rogue": {"aggressiveness": 50, "honesty": 30, "loyalty": 40, "caution": 65},
            "mage": {"aggressiveness": 40, "honesty": 60, "loyalty": 55, "caution": 70},
            "paladin": {"aggressiveness": 60, "honesty": 85, "loyalty": 90, "caution": 40},
            "cleric": {"aggressiveness": 35, "honesty": 80, "loyalty": 85, "caution": 55},
            "archer": {"aggressiveness": 55, "honesty": 70, "loyalty": 60, "caution": 70},
            "merchant": {"aggressiveness": 25, "honesty": 50, "loyalty": 45, "caution": 60},
            "assassin": {"aggressiveness": 70, "honesty": 20, "loyalty": 30, "caution": 75},
            "bard": {"aggressiveness": 40, "honesty": 55, "loyalty": 50, "caution": 45},
            "ranger": {"aggressiveness": 60, "honesty": 75, "loyalty": 65, "caution": 60},
            "monk": {"aggressiveness": 50, "honesty": 85, "loyalty": 80, "caution": 50},
            "warlock": {"aggressiveness": 65, "honesty": 35, "loyalty": 25, "caution": 55},
        }
        
        values = profession_values.get(profession_name, {
            "aggressiveness": 50,
            "honesty": 50,
            "loyalty": 50,
            "caution": 50
        }).copy()
        
        # Modificar según rasgos de personalidad
        trait_modifiers = {
            "aggressive": {"aggressiveness": 20},
            "timid": {"aggressiveness": -20, "caution": 15},
            "brave": {"caution": -10, "aggressiveness": 10},
            "cowardly": {"caution": 20, "aggressiveness": -15},
            "honest": {"honesty": 25},
            "cunning": {"honesty": -20},
            "manipulative": {"honesty": -25},
            "loyal": {"loyalty": 25},
            "treacherous": {"loyalty": -30},
            "cautious": {"caution": 15},
            "reckless": {"caution": -20},
            "impulsive": {"caution": -10, "aggressiveness": 5},
            "ruthless": {"aggressiveness": 15, "honesty": -10},
            "compassionate": {"aggressiveness": -10, "honesty": 10},
        }
        
        for trait_id, intensity in personality.items():
            if trait_id in trait_modifiers:
                modifiers = trait_modifiers[trait_id]
                # Aplicar modificadores escalados por intensidad (0-100)
                scale = intensity / 100.0
                for value_name, modifier in modifiers.items():
                    if value_name in values:
                        values[value_name] += int(modifier * scale)
        
        # Asegurar que todos los valores estén en rango [0-100]
        for key in values:
            values[key] = max(0, min(100, values[key]))
        
        return values
    
    def add_personality_trait(self, trait_name, trait_intensity):
        """
        Agrega o modifica un rasgo de personalidad.
        
        Args:
            trait_name: ID del rasgo
            trait_intensity: Intensidad (0-100)
        """
        self.personality[trait_name] = max(0, min(100, trait_intensity))
    
    def get_personality_summary(self):
        """
        Retorna un resumen legible de la personalidad del NPC.
        
        Returns:
            String con descripción de personalidad
        """
        with open(DATA / "personality_traits.json", encoding="utf-8") as f:
            personality_data = json.load(f)
        
        traits_dict = {t["id"]: t for t in personality_data["traits"]}
        
        summary = []
        for trait_id, intensity in sorted(
            self.personality.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            if trait_id in traits_dict:
                trait_name = traits_dict[trait_id].get("name", trait_id)
                summary.append(f"{trait_name} ({intensity})")
        
        return ", ".join(summary)
    
    def get_npc_values_summary(self):
        """
        Retorna un resumen de los valores únicos del NPC.
        
        Returns:
            String con descripción de valores
        """
        summary = []
        for value_name, value_level in sorted(
            self.npc_values.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            summary.append(f"{value_name}: {value_level}")
        
        return " | ".join(summary)
    
    def would_initiate_combat(self):
        """
        Determina probabilísticamente si el NPC iniciaría un combate.
        Basado en aggressiveness, bravery y caution.
        
        Returns:
            True si el NPC debería iniciar combate, False en caso contrario
        """
        aggressiveness = self.npc_values.get("aggressiveness", 50)
        caution = self.npc_values.get("caution", 50)
        
        # Probabilidad = (aggressiveness - caution) / 100
        combat_probability = (aggressiveness - caution) / 100.0
        combat_probability = max(0.0, min(1.0, combat_probability))
        
        return random.random() < combat_probability
    
    def would_betray(self):
        """
        Determina probabilísticamente si el NPC traicionaría.
        Basado en loyalty, honesty y cunning.
        
        Returns:
            True si el NPC debería traicionar, False en caso contrario
        """
        loyalty = self.npc_values.get("loyalty", 50)
        honesty = self.npc_values.get("honesty", 50)
        
        # Probabilidad de traición = (100 - loyalty) / 100
        betrayal_probability = (100 - loyalty) / 100.0
        betrayal_probability = max(0.0, min(1.0, betrayal_probability))
        
        return random.random() < betrayal_probability
    
    def __repr__(self):
        """Representación en string del NPC."""
        return (
            f"NPC(name={self.name}, profession={self.profession_display}, "
            f"race={self.race}, level={self.level})"
        )
