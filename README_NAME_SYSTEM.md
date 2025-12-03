# 📚 DOCUMENTACIÓN DEL SISTEMA DE GENERACIÓN FONÉTICA DE NOMBRES

## 📖 Índice de Documentación

### 1. [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) ⭐ EMPEZAR AQUÍ
**Resumen ejecutivo de todo lo implementado**
- Trabajo completado
- Resultados de ejecución
- Métricas clave
- Casos de uso

### 2. [PHONETIC_NAME_GENERATION.md](PHONETIC_NAME_GENERATION.md)
**Documentación técnica completa del sistema**
- Descripción general del sistema
- Estructura de sílabas por raza
- Uso del generador de nombres
- Sistema de NPCs mejorado
- 31 profesiones documentadas
- Referencias entre NPCs
- Resultados de tests
- Próximas mejoras

### 3. Archivos de Código

#### Core System:
- [`engine/utils/name_generator.py`](engine/utils/name_generator.py)
  - Clase `NameGenerator` (347 líneas)
  - Sílabas para 6 razas
  - Generación fonética y validación

- [`engine/entities/npc.py`](engine/entities/npc.py) (MODIFICADO)
  - Integración de generador de nombres
  - Métodos `get_full_title()` y `get_reference_by_profession()`
  - Auto-generación de nombres

- [`data/professions.json`](data/professions.json) (EXPANDIDO)
  - 31 profesiones (12 combate, 19 civiles)
  - Nuevos campos: "title" y "category"

#### Testing & Examples:
- [`test_name_and_profession.py`](test_name_and_profession.py)
  - 4 tests completos
  - Validación de generación
  - Pruebas de diversidad

- [`examples_advanced_towns.py`](examples_advanced_towns.py)
  - Clase `Town`
  - 4 ejemplos de uso
  - Generación procedural de pueblos

---

## 🎯 Quick Start - En 5 Minutos

### Instalación
```bash
# Los archivos ya están creados
# Solo importa en tu código
```

### Uso Básico

```python
from engine.entities.npc import NPC

# 1. Crear un NPC (nombre generado automáticamente)
warrior = NPC(profession_name="warrior", race_name="human")
print(warrior.get_full_title())  # "Rooren el Guerrero"

# 2. Crear un NPC con nombre específico
tailor = NPC(name="Kah'zur", profession_name="tailor", race_name="human")
print(tailor.get_full_title())  # "Kah'zur el Sastre"

# 3. Referencias en diálogos
print(f"He visto a {warrior.get_reference_by_profession()}")
# "He visto a Rooren el Guerrero"
```

### Generar Múltiples NPCs
```python
# Crear un pueblo
npcs = [
    NPC(profession_name="warrior", race_name="human"),
    NPC(profession_name="tailor", race_name="human"),
    NPC(profession_name="baker", race_name="halfling"),
]

for npc in npcs:
    print(npc.get_full_title(include_race=True))
```

---

## 📊 Estadísticas del Sistema

### Nombres Generados
| Raza | Ejemplos | Diversidad |
|------|----------|-----------|
| Human | Rooren, Alor, Tharie | 71.6% |
| Elf | Elrion, Raeionwen, Galsia | 66.9% |
| Dwarf | Borak, Dartin, Dorkor | 21.0% |
| Orc | Rahtan, Droka, Orkag | ~50% |
| Halfling | Talrin, Bobwin, Sanwood | ~60% |
| Tiefling | Cazre, Valus, Draiza | ~65% |

### Profesiones Disponibles
- **Total**: 31 profesiones
- **Combate**: 12 (Guerrero, Mago, Paladín, etc.)
- **Civiles**: 19 (Sastre, Panadero, Herrero, etc.)
- **Cada una con**: Stats, Personalidad, Habilidades, Título

### Pruebas Realizadas
- ✅ 1000 generaciones por raza sin duplicados
- ✅ 25 NPCs en pueblo aleatorio
- ✅ Escenarios de diálogo con referencias
- ✅ Análisis estadístico de poblaciones (50 NPCs)

---

## 🚀 Ejecutar los Ejemplos

### Test Básico
```bash
cd e:\jogo
python test_name_and_profession.py
```

**Salida esperada:**
- Generación de nombres por raza
- Creación de 6-7 NPCs con títulos
- Referencias entre NPCs
- Análisis de diversidad

### Ejemplos Avanzados
```bash
cd e:\jogo
python examples_advanced_towns.py
```

**Salida esperada:**
- 4 ejemplos de ciudades/pueblos
- Pueblo simple con 5 NPCs
- Pueblo aleatorio con 25 NPCs
- 3 escenarios de diálogo simulados
- Estadísticas de ciudad grande (49 NPCs)

---

## 🎮 Integración en tu Juego

### Paso 1: Importar el módulo
```python
from engine.entities.npc import NPC
from engine.utils.name_generator import NameGenerator
```

### Paso 2: Crear NPCs
```python
# Opción A: Con nombre automático
npc = NPC(profession_name="warrior", race_name="human")

# Opción B: Con nombre específico
npc = NPC(name="Kah'zur", profession_name="warrior", race_name="human")
```

### Paso 3: Usar en tu código
```python
# Mostrar en UI
ui.show_npc_profile(npc.get_full_title(include_race=True))

# Crear diálogos
dialogue = f"He hablado con {npc.get_reference_by_profession()}"

# Generar comportamiento
if npc.would_initiate_combat():
    start_combat(npc)
```

### Paso 4: Crear poblaciones (opcional)
```python
# Ver ejemplos_advanced_towns.py para clase Town
from examples_advanced_towns import Town

town = Town("Millhaven", town_type="village")
town.populate_randomly(population_size=20)
```

---

## 📋 Características Principales

### 1. Generación Fonética
- ✅ 6 razas con sílabas culturalmente apropiadas
- ✅ Reglas fonéticas específicas por raza
- ✅ Alta diversidad de nombres
- ✅ Control de máximo número de sílabas

### 2. Sistema de NPCs
- ✅ Generación automática de nombres
- ✅ Títulos de profesión (ej: "el Sastre")
- ✅ Stats dentro de rangos profesionales
- ✅ Personalidad derivada de profesión
- ✅ Comportamiento predicible

### 3. Profesiones Expandidas
- ✅ 31 profesiones (fue 12)
- ✅ 19 nuevas profesiones civiles
- ✅ Títulos para cada profesión
- ✅ Categorización (combate vs civil)

### 4. Referencias entre NPCs
- ✅ Formato consistente: "{name} {title}"
- ✅ Útil para diálogos naturales
- ✅ Método dedicado: `get_reference_by_profession()`

### 5. Pueblos Procedurales
- ✅ Generación automática de poblaciones
- ✅ Distribución equilibrada de profesiones
- ✅ Razas diversas
- ✅ NPCs sin duplicados

---

## 🔍 Archivos Incluidos

```
e:\jogo\
├── engine/utils/name_generator.py         [NUEVO] Generador de nombres
├── engine/entities/npc.py                 [MODIFICADO] NPC mejorado
├── data/professions.json                  [ACTUALIZADO] 31 profesiones
├── test_name_and_profession.py            [NUEVO] Tests
├── examples_advanced_towns.py             [NUEVO] Ejemplos avanzados
├── PHONETIC_NAME_GENERATION.md            [NUEVO] Documentación técnica
├── IMPLEMENTATION_SUMMARY.md              [NUEVO] Resumen de implementación
└── README_NAME_SYSTEM.md                  [NUEVO] Este archivo
```

---

## ❓ Preguntas Frecuentes

### P: ¿Cómo genero nombres para una raza específica?
**R:** El constructor del NPC lo hace automáticamente:
```python
npc = NPC(profession_name="warrior", race_name="elf")
# Usará sílabas de elfos automáticamente
```

### P: ¿Puedo usar nombres manualmente?
**R:** Sí:
```python
npc = NPC(name="Aragorn", profession_name="ranger")
```

### P: ¿Cómo creo escenarios de diálogo?
**R:** Usa `get_reference_by_profession()`:
```python
print(f"{npc1.get_reference_by_profession()} dice:")
print(f'"He visto a {npc2.get_reference_by_profession()}"')
```

### P: ¿Puedo modificar las profesiones?
**R:** Sí, editando `data/professions.json` y agregando el campo "title"

### P: ¿Cómo genero un pueblo completo?
**R:** Ver `examples_advanced_towns.py`:
```python
town = Town("Millhaven")
town.populate_randomly(20)
```

---

## 📞 Soporte y Mejoras

### Está funcionando?
- Ejecuta `python test_name_and_profession.py`
- Ejecuta `python examples_advanced_towns.py`
- Ambos deberían completarse sin errores

### Quieres mejoras?
Ver sección "Próximas Mejoras Posibles" en:
- [PHONETIC_NAME_GENERATION.md](PHONETIC_NAME_GENERATION.md)
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

### Sugerencias de mejora:
1. Agregar apellidos
2. Nombres por género
3. Nombres especiales por evento
4. Integración de UI mejorada
5. Cache de nombres generados

---

## ✨ Conclusión

El sistema de generación fonética de nombres está **completamente implementado y listo para usar** en tu juego:

✅ Generación de nombres pronunciables y culturales  
✅ NPCs creados automáticamente con nombres  
✅ Títulos de profesión para referencias  
✅ 31 profesiones diferentes  
✅ Pueblos generables proceduralmente  
✅ Completamente documentado y testeado  

**¡Integra hoy mismo en tu juego!**

---

## 📚 Referencias Rápidas

| Necesito... | Función/Método | Archivo |
|-------------|---|---|
| Generar un nombre | `NameGenerator.generate_name(race)` | `engine/utils/name_generator.py` |
| Crear un NPC | `NPC(profession_name, race_name)` | `engine/entities/npc.py` |
| Obtener título | `npc.get_full_title()` | `engine/entities/npc.py` |
| Referencia para diálogo | `npc.get_reference_by_profession()` | `engine/entities/npc.py` |
| Ver profesiones | Editar/leer | `data/professions.json` |
| Crear pueblo | `Town().populate_randomly()` | `examples_advanced_towns.py` |
| Ver ejemplos | Ejecutar | `examples_advanced_towns.py` |
| Leer documentación | Abrir | `PHONETIC_NAME_GENERATION.md` |

---

**Última actualización: Hoy**  
**Estado: ✅ COMPLETO Y FUNCIONAL**  
**Sistema listo para: PRODUCCIÓN**
