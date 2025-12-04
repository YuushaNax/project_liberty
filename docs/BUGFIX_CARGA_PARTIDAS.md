# BUGFIX - Carga de Partidas

## Problema Reportado

Al intentar cargar una partida, se mostraba el siguiente error:
```
pygame has no attribute called "k_f5"
```

Esto ocurría varias veces hasta que finalmente cargaba la partida.

## Causa Raíz

### Bug 1: Tecla con nombre incorrecto
En `interface/screens/exploration.py` línea 139, se usaba:
```python
elif event.key == pg.K_f5:  # ❌ INCORRECTO (minúsculas)
```

Pygame define las constantes de teclas con **mayúsculas**:
```python
elif event.key == pg.K_F5:  # ✅ CORRECTO (mayúsculas)
```

### Bug 2: Posición no se restauraba correctamente
En `engine/world/world.py`, el método `load_game()` restauraba la posición pero luego era sobrescrita por `generate_world()` que buscaba una nueva posición inicial.

```python
# ANTES (incorrecto):
pos = save_data["world"]["player_position"]
self.player_world_x = pos["x"]
self.player_world_y = pos["y"]
self.player_data = save_data.get("player", {})
self.generate_world()  # ❌ Sobrescribía la posición
self.load_local_map()

# DESPUÉS (correcto):
pos = save_data["world"]["player_position"]
saved_x = pos["x"]
saved_y = pos["y"]
self.player_data = save_data.get("player", {})
self.generate_world()  # Generar mundo
self.player_world_x = saved_x  # ✅ Restaurar posición guardada
self.player_world_y = saved_y
self.load_local_map()
```

## Soluciones Implementadas

### ✅ Fix 1: Cambiar tecla F5 a mayúsculas
**Archivo:** `interface/screens/exploration.py` línea 139
```python
# Cambio:
elif event.key == pg.K_f5:  # ❌
↓↓↓
elif event.key == pg.K_F5:  # ✅
```

### ✅ Fix 2: Restaurar posición DESPUÉS de generar mundo
**Archivo:** `engine/world/world.py` línea 310-348

El orden correcto es:
1. Leer datos guardados (including posición)
2. Generar mundo con misma semilla
3. Restaurar posición guardada
4. Cargar mapa local

## Verificación

✅ Prueba de teclas: Todos los K_F* están disponibles en pygame
✅ Prueba de carga: Posición se restaura correctamente
✅ Prueba de persistencia: Todas las pruebas pasan
✅ Prueba de sesiones: 2 sesiones cargadas sin errores

### Resultados de Test

```
[OK] Archivo encontrado
[OK] Datos guardados:
    - Semilla: 442167797
    - Posición: (65, 81)
    - Jugador: kjkhbg

[OK] Partida cargada correctamente
[OK] Posicion restaurada: (65, 81)  ✅ IGUAL QUE GUARDADA
[OK] Datos del jugador: kjkhbg
```

## Impacto

- ✅ No más error de `pygame has no attribute called "k_f5"`
- ✅ Posición se restaura correctamente al cargar
- ✅ Carga de partidas funciona sin interrupciones
- ✅ Múltiples sesiones se cargan correctamente

## Archivos Modificados

1. `interface/screens/exploration.py` - Línea 139 (tecla F5)
2. `engine/world/world.py` - Líneas 310-348 (restauración de posición)

---

**Estado: CORREGIDO ✅**
