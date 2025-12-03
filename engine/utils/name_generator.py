# engine/utils/name_generator.py
"""
Generador fonético de nombres para NPCs y personajes.
Utiliza sílabas y reglas fonéticas específicas por raza.
"""

import random
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA = BASE_DIR / "data"

# Definición de sílabas por raza (estructura fonética)
RACE_SYLLABLES = {
    "human": {
        "prefixes": ["Ar", "El", "Th", "Br", "Al", "Ed", "Ga", "Ha", "Ro", "Jo", "Ma", "No", "Re", "So", "To", "Vi", "Wa", "Za"],
        "middles": ["ald", "an", "bert", "ian", "ol", "in", "us", "eth", "or", "ar", "en", "ew", "im", "om", "ys", "il"],
        "suffixes": ["o", "a", "e", "us", "ia", "an", "er", "or", "en", "yn", "ay", "ey", "ow", "ie", "el", "ael"],
        "rules": {
            "avoid_double_consonants": True,
            "prefer_vowel_end": False,
            "max_syllables": 3
        }
    },
    "elf": {
        "prefixes": ["Aer", "Cel", "Elr", "Gal", "Lar", "Lae", "Rae", "Sil", "Tae", "Tel", "Val", "Vel", "Ael", "Ith", "Orn", "Syn"],
        "middles": ["a", "e", "i", "an", "en", "eth", "iel", "ion", "las", "lin", "nes", "oth", "uin", "vel"],
        "suffixes": ["on", "an", "or", "ar", "eth", "ion", "ael", "iel", "wen", "win", "lin", "nis", "ryn", "sia", "tel"],
        "rules": {
            "avoid_double_consonants": True,
            "prefer_vowel_end": True,
            "max_syllables": 3,
            "vowel_heavy": True
        }
    },
    "dwarf": {
        "prefixes": ["Bal", "Bor", "Dal", "Dar", "Dha", "Dor", "Dur", "Flor", "Gar", "Grim", "Gun", "Khar", "Khor", "Thor", "Thro"],
        "middles": ["ak", "an", "ar", "ir", "om", "or", "un", "ak", "ald", "eth", "in", "ord"],
        "suffixes": ["ak", "an", "ar", "ax", "eth", "in", "or", "un", "ald", "ath", "kor", "son", "tin", "win"],
        "rules": {
            "avoid_double_consonants": False,
            "prefer_vowel_end": False,
            "max_syllables": 2,
            "consonant_heavy": True
        }
    },
    "orc": {
        "prefixes": ["Dro", "Gro", "Gul", "Gra", "Gri", "Gor", "Og", "Ork", "Rah", "Rog", "Rok", "Tha", "Tho", "Urg", "Uz"],
        "middles": ["ak", "ar", "og", "ul", "agh", "rak", "rog", "ug", "ugh", "ah", "ag", "og", "ur"],
        "suffixes": ["ak", "an", "ar", "ag", "agh", "og", "rak", "tan", "ug", "ush", "uz", "ka", "kha"],
        "rules": {
            "avoid_double_consonants": False,
            "prefer_vowel_end": False,
            "max_syllables": 2,
            "guttural": True
        }
    },
    "halfling": {
        "prefixes": ["Bil", "Bob", "Cal", "Dar", "Fig", "Ful", "Ger", "Hob", "Ilo", "Per", "Pip", "Ral", "Rin", "Ros", "San", "Tal"],
        "middles": ["ba", "bo", "da", "di", "fa", "fi", "go", "ja", "lo", "mo", "na", "po", "ra", "ri", "sa", "ti"],
        "suffixes": ["a", "an", "en", "er", "in", "lyn", "o", "on", "or", "rin", "son", "ton", "win", "wood"],
        "rules": {
            "avoid_double_consonants": True,
            "prefer_vowel_end": True,
            "max_syllables": 2,
            "shorter": True
        }
    },
    "tiefling": {
        "prefixes": ["Aza", "Caz", "Des", "Dra", "Far", "Hor", "Iza", "Kaz", "Lar", "Mal", "Naz", "Raz", "Val", "Vel", "Xan", "Zig"],
        "middles": ["ar", "az", "el", "er", "ia", "ir", "is", "iz", "or", "ra", "re", "us"],
        "suffixes": ["a", "an", "ar", "az", "el", "era", "eth", "ia", "is", "iz", "or", "ra", "re", "us", "uz"],
        "rules": {
            "avoid_double_consonants": False,
            "prefer_vowel_end": True,
            "max_syllables": 3,
            "exotic": True
        }
    }
}

# Títulos de oficio por género
PROFESSION_TITLES = {
    "male": {},
    "female": {},
    "neutral": {}
}


class NameGenerator:
    """Generador de nombres fonético para NPCs."""
    
    def __init__(self):
        """Inicializa el generador de nombres."""
        self.syllables = RACE_SYLLABLES
    
    def generate_name(self, race="human", gender=None, seed=None):
        """
        Genera un nombre fonético para un NPC.
        
        Args:
            race: Raza del NPC (human, elf, dwarf, orc, halfling, tiefling)
            gender: Género (no afecta el nombre, solo para futura expansión)
            seed: Semilla para reproducibilidad
        
        Returns:
            Nombre generado
        """
        if seed is not None:
            random.seed(seed)
        
        # Validar raza
        if race not in self.syllables:
            race = "human"
        
        syllable_set = self.syllables[race]
        rules = syllable_set.get("rules", {})
        max_syllables = rules.get("max_syllables", 3)
        
        # Decidir número de sílabas
        num_syllables = random.randint(2, max_syllables)
        
        # Construir nombre
        name_parts = []
        
        # Prefijo (siempre)
        prefix = random.choice(syllable_set["prefixes"])
        name_parts.append(prefix)
        
        # Medios (según número de sílabas)
        for i in range(num_syllables - 2):
            middle = random.choice(syllable_set["middles"])
            name_parts.append(middle)
        
        # Sufijo (siempre)
        suffix = random.choice(syllable_set["suffixes"])
        name_parts.append(suffix)
        
        # Combinar partes
        name = "".join(name_parts)
        
        # Aplicar reglas
        if rules.get("avoid_double_consonants", True):
            name = self._remove_double_consonants(name)
        
        # Capitalizar
        name = name.capitalize()
        
        return name
    
    def _remove_double_consonants(self, name):
        """Elimina consonantes duplicadas consecutivas."""
        vowels = set("aeiouAEIOU")
        result = []
        
        for i, char in enumerate(name):
            if i == 0:
                result.append(char)
            elif char not in vowels and char == name[i-1]:
                # Skip duplicate consonants
                continue
            else:
                result.append(char)
        
        return "".join(result)
    
    def generate_multiple_names(self, race="human", count=5):
        """
        Genera múltiples nombres para una raza.
        
        Args:
            race: Raza del NPC
            count: Cantidad de nombres a generar
        
        Returns:
            Lista de nombres
        """
        names = []
        seen = set()
        
        attempts = 0
        while len(names) < count and attempts < count * 10:
            name = self.generate_name(race)
            if name not in seen:
                names.append(name)
                seen.add(name)
            attempts += 1
        
        return names
    
    @staticmethod
    def get_profession_title(profession_name, gender="neutral"):
        """
        Obtiene el título de oficio para un NPC.
        
        Args:
            profession_name: Nombre de la profesión
            gender: Género (neutral por defecto)
        
        Returns:
            Título formateado (ej: "el Sastre", "la Sastre")
        """
        with open(DATA / "professions.json", encoding="utf-8") as f:
            professions = json.load(f)
        
        profession = next(
            (p for p in professions if p["profession_name"] == profession_name),
            None
        )
        
        if not profession:
            return f"el {profession_name.capitalize()}"
        
        title = profession.get("title", f"el {profession.get('display', profession_name)}")
        
        # Ajustar por género
        if gender == "female":
            # Convertir "el" a "la", "el Sastre" a "la Sastre/Sastra"
            if title.startswith("el "):
                title = "la " + title[3:]
        
        return title


# Crear instancia global
name_generator = NameGenerator()


if __name__ == "__main__":
    # Test del generador
    print("=" * 60)
    print("TEST DE GENERACIÓN DE NOMBRES")
    print("=" * 60)
    
    gen = NameGenerator()
    
    for race in ["human", "elf", "dwarf", "orc", "halfling", "tiefling"]:
        print(f"\n{race.upper()}:")
        names = gen.generate_multiple_names(race, 5)
        for name in names:
            print(f"  - {name}")
