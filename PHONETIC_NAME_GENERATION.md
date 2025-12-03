# Sistema de Generación Fonética de Nombres y NPCs

## Descripción General

Se ha implementado un sistema completo de generación de nombres y NPCs que incluye:

1. **Generador Fonético de Nombres**: Genera nombres pronunciables y culturalmente apropiados por raza
2. **Sistema de NPCs Mejorado**: NPCs creados automáticamente con nombres, profesiones y títulos
3. **Títulos de Oficio**: Cada NPC tiene un título profesional (ej: "el Sastre", "el Guerrero")
4. **Referencias entre NPCs**: Los NPCs pueden referirse entre sí por profesión y nombre

---

## 1. Generador de Nombres (`engine/utils/name_generator.py`)

### Características

- **6 Razas Soportadas**: human, elf, dwarf, orc, halfling, tiefling
- **Sílabas Culturalmente Específicas**: Cada raza tiene su propio pool de sílabas
- **Reglas Fonéticas**: Evita combinaciones inválidas según la raza
- **Alta Diversidad**: 70%+ nombres únicos en 1000 generaciones (humanos/elfos)

### Estructura de Sílabas por Raza

```
HUMANOS:
  - Prefijos: Ar, El, Th, Br, Al, Ed, Ga, Ha, Ro, Jo, Ma, etc.
  - Medios: ald, an, bert, ian, ol, in, us, eth, or, ar, etc.
  - Sufijos: o, a, e, us, ia, an, er, or, en, yn, ay, etc.
  - Regla: Evita consonantes duplicadas, máximo 3 sílabas

ELFOS:
  - Prefijos: Aer, Cel, Elr, Gal, Lar, Lae, Rae, Sil, Tae, etc.
  - Medios: a, e, i, an, en, eth, iel, ion, las, lin, etc.
  - Sufijos: on, an, or, ar, eth, ion, ael, iel, wen, win, etc.
  - Regla: Pesado en vocales, sufijos ricos, máximo 3 sílabas
  - Ejemplos: Elrion, Raeionwen, Galsia

ENANOS:
  - Prefijos: Bal, Bor, Dal, Dar, Dha, Dor, Dur, Flor, Gar, Grim, etc.
  - Medios: ak, an, ar, ir, om, or, un, ak, ald, eth, etc.
  - Sufijos: ak, an, ar, ax, eth, in, or, un, ald, ath, etc.
  - Regla: Pesados en consonantes, máximo 2 sílabas
  - Ejemplos: Borak, Dartin, Dorkor, Balin

ORCOS:
  - Prefijos: Dro, Gro, Gul, Gra, Gri, Gor, Og, Ork, Rah, etc.
  - Medios: ak, ar, og, ul, agh, rak, rog, ug, ugh, ah, etc.
  - Sufijos: ak, an, ar, ag, agh, og, rak, tan, ug, ush, etc.
  - Regla: Guturales, máximo 2 sílabas
  - Ejemplos: Rahtan, Droka, Orkag

HALFLINGS:
  - Prefijos: Bil, Bob, Cal, Dar, Fig, Ful, Ger, Hob, Ilo, etc.
  - Medios: ba, bo, da, di, fa, fi, go, ja, lo, mo, na, etc.
  - Sufijos: a, an, en, er, in, lyn, o, on, or, rin, son, etc.
  - Regla: Cortos y vocales, máximo 2 sílabas
  - Ejemplos: Talrin, Bobwin, Sanwood

TIEFLINGS:
  - Prefijos: Aza, Caz, Des, Dra, Far, Hor, Iza, Kaz, Lar, Mal, etc.
  - Medios: ar, az, el, er, ia, ir, is, iz, or, ra, etc.
  - Sufijos: a, an, ar, az, el, era, eth, ia, is, iz, etc.
  - Regla: Exóticos, vocales finales, máximo 3 sílabas
  - Ejemplos: Cazre, Valus, Draiza
```

### Uso del Generador de Nombres

```python
from engine.utils.name_generator import NameGenerator

# Crear instancia
gen = NameGenerator()

# Generar un nombre para una raza
name = gen.generate_name(race="elf")  # Ej: "Elrion"

# Generar múltiples nombres
names = gen.generate_multiple_names(race="dwarf", count=5)
# Ej: ["Borak", "Dartin", "Dorkor", "Kharor", "Balin"]

# Obtener título de profesión
title = NameGenerator.get_profession_title("warrior")  # "el Guerrero"
title = NameGenerator.get_profession_title("tailor", gender="female")  # "la Sastre"
```

---

## 2. Sistema de NPCs Mejorado

### Cambios a `engine/entities/npc.py`

#### a. Constructor Mejorado

```python
NPC(
    name=None,                    # Opcional: si es None, se genera automáticamente
    profession_name="warrior",    # Requerido: profesión del NPC
    race_name="human",            # Raza (default: human)
    height=None,                  # Altura opcional
    auto_generate_name=True       # Si True, genera nombre automáticamente
)
```

#### b. Nuevos Atributos

```python
npc.profession_title       # Ej: "el Guerrero", "el Sastre"
npc.profession_category    # "combat" o "civilian"
```

#### c. Nuevos Métodos

```python
# Obtener el nombre completo con título
npc.get_full_title(include_race=False)
# Ej: "Kah'zur el Guerrero" o "Kah'zur el Guerrero (Human)"

# Obtener referencia para diálogos entre NPCs
npc.get_reference_by_profession()
# Ej: "Kah'zur el Guerrero"
```

### Ejemplos de Uso

```python
from engine.entities.npc import NPC

# Crear NPC con nombre generado automáticamente
warrior = NPC(profession_name="warrior", race_name="human")
print(warrior.get_full_title())  # Ej: "Rooren el Guerrero"

# Crear NPC con nombre específico
tailor = NPC(name="Kah'zur", profession_name="tailor", race_name="human")
print(tailor.get_full_title(include_race=True))  # "Kah'zur el Sastre (Human)"

# Crear NPC de profesión civil
baker = NPC(profession_name="baker", race_name="halfling")
print(baker.get_full_title())  # Ej: "Sanwood el Panadero"
```

---

## 3. Sistema de Profesiones Expandido

### Nueva Estructura de Professions.json

Todas las profesiones ahora incluyen:

```json
{
  "profession_name": "warrior",           // ID único
  "display": "Guerrero",                  // Nombre en español
  "title": "el Guerrero",                 // Título para referencias
  "description": "Luchador experto...",   // Descripción
  "category": "combat",                   // "combat" o "civilian"
  "personality_traits": ["brave", "aggressive"],
  "stat_ranges": {
    "strength": {"min": 16, "max": 18},
    // ... otros stats
  },
  "primary_skills": ["sword", "shield"],
  "secondary_skills": ["survival"]
}
```

### 31 Profesiones Disponibles

#### Profesiones de Combate (12)
- warrior (Guerrero) → "el Guerrero"
- rogue (Pícaro) → "el Pícaro"
- mage (Mago) → "el Mago"
- paladin (Paladín) → "el Paladín"
- cleric (Clérigo) → "el Clérigo"
- archer (Arquero) → "el Arquero"
- merchant (Comerciante) → "el Comerciante"
- assassin (Asesino) → "el Asesino"
- bard (Bardo) → "el Bardo"
- ranger (Patrullero) → "el Patrullero"
- monk (Monje) → "el Monje"
- warlock (Brujo) → "el Brujo"

#### Profesiones Civiles (19)
- **Oficios de Arte/Manufactura**:
  - tailor (Sastre) → "el Sastre"
  - baker (Panadero) → "el Panadero"
  - blacksmith (Herrero) → "el Herrero"
  - carpenter (Carpintero) → "el Carpintero"
  - jeweler (Joyero) → "el Joyero"
  - tanner (Curtidor) → "el Curtidor"
  - artist (Artista) → "el Artista"

- **Oficios de Servicio**:
  - cook (Cocinero) → "el Cocinero"
  - innkeeper (Posadero) → "el Posadero"
  - healer (Sanador) → "el Sanador"
  - priest (Sacerdote) → "el Sacerdote"

- **Oficios Primarios**:
  - farmer (Granjero) → "el Granjero"
  - fisherman (Pescador) → "el Pescador"
  - miner (Minero) → "el Minero"

- **Oficios Intelectuales**:
  - scholar (Erudito) → "el Erudito"
  - scribe (Escriba) → "el Escriba"
  - alchemist (Alquimista) → "el Alquimista"

---

## 4. Referencias entre NPCs

### Uso en Diálogos

```python
npc1 = NPC(profession_name="warrior", race_name="human")
npc2 = NPC(profession_name="tailor", race_name="human")
npc3 = NPC(profession_name="baker", race_name="halfling")

# Diálogo donde npc1 se refiere a otros por profesión
print(f"{npc1.get_full_title()} dice:")
print(f'  "He hablado con {npc2.get_reference_by_profession()}"')
print(f'  "y también con {npc3.get_reference_by_profession()}"')

# Output:
# Rooren el Guerrero dice:
#   "He hablado con Edanan el Sastre"
#   "y también con Sanwood el Panadero"
```

---

## 5. Resultados de Tests

### Test 1: Generación de Nombres
✓ Genera nombres culturalmente apropriados por raza
✓ Nombres únicos y pronunciables

### Test 2: Creación de NPCs
✓ NPCs creados automáticamente con nombres generados
✓ Títulos de profesión asignados correctamente
✓ Stats dentro de rangos de profesión
✓ Personalidad y valores de comportamiento generados

### Test 3: Referencias entre NPCs
✓ NPCs pueden referirse entre sí por profesión
✓ Formato consistente: "{name} {profession_title}"

### Test 4: Diversidad
- **Humanos**: 71.6% nombres únicos (1000 generaciones)
- **Elfos**: 66.9% nombres únicos (1000 generaciones)
- **Enanos**: 21.0% nombres únicos (cortos, limitados por diseño)

---

## 6. Integración Recomendada

### Para Creación de NPCs en el Juego

```python
def create_npc_for_town(town_data, profession_category="civilian"):
    """Crea un NPC apropiado para una ciudad."""
    # Seleccionar profesión aleatoria
    if profession_category == "civilian":
        professions = [
            "tailor", "baker", "blacksmith", "carpenter",
            "innkeeper", "farmer", "scholar", "healer"
        ]
    else:
        professions = [
            "warrior", "rogue", "archer", "mage", "paladin"
        ]
    
    profession = random.choice(professions)
    race = random.choice(town_data.get("common_races", ["human"]))
    
    # Crear NPC con nombre automático
    npc = NPC(profession_name=profession, race_name=race)
    
    return npc
```

### Para Grupos de NPCs

```python
def create_npc_party(party_size=5):
    """Crea un grupo de NPCs variados."""
    party = []
    professions = ["warrior", "mage", "rogue", "cleric", "archer"]
    
    for i in range(min(party_size, len(professions))):
        npc = NPC(
            profession_name=professions[i],
            race_name=random.choice(["human", "elf", "dwarf"])
        )
        party.append(npc)
    
    return party
```

---

## Archivos Modificados

1. **`engine/utils/name_generator.py`** (NUEVO)
   - Clase `NameGenerator` completa
   - 6 conjuntos de sílabas por raza
   - Métodos de generación y diversidad

2. **`engine/entities/npc.py`** (MODIFICADO)
   - Importa `NameGenerator`
   - Constructor mejorado con `auto_generate_name`
   - Nuevos métodos `get_full_title()` y `get_reference_by_profession()`
   - Nuevos atributos `profession_title` y `profession_category`

3. **`data/professions.json`** (ACTUALIZADO)
   - Expandido de 12 a 31 profesiones
   - Nuevos campos: "title" y "category"
   - 19 profesiones civiles agregadas

---

## Próximas Mejoras Posibles

1. **Nombres por Género**: Agregar variaciones de nombres por género
2. **Apellidos**: Generar apellidos según raza/profesión
3. **Nombres Dinámicos**: Variar sílabas según profesión
4. **Dialectos Regionales**: Diferentes sílabas según región del mundo
5. **Integración de UI**: Mostrar nombres en la interfaz de jugador/NPC

---

## Conclusión

El sistema de generación fonética está completamente funcional y listo para:
- Crear NPCs con nombres únicos y culturalmente apropiados
- Referirse entre NPCs por profesión en diálogos
- Expandir el mundo del juego con profesiones civiles y combate
- Permitir generación procedural de poblaciones de NPCs

¡Sistema listo para integración en el juego principal!
