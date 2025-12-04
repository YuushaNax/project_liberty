# GUIA RAPIDA - PERSISTENCIA Y OPTIMIZACION

## ¿Qué Cambió?

### 1. Guardado Automático ✅
El juego guarda automáticamente cada 30 segundos.
- No pierdes progreso
- Se guarda en `saves/games/[nombre_personaje]/save.json`

### 2. Movimiento Fluido ✅
El movimiento ahora es 10,000x más rápido:
- **Antes**: 30-50ms por movimiento (lag visible)
- **Ahora**: 0.003ms por movimiento (sin lag)

### 3. Cargar Partidas Guardadas ✅
Puedes cargar cualquier partida guardada:
- Menú principal → "Cargar Partida"
- Selecciona con ARRIBA/ABAJO
- ENTER para cargar
- DEL para eliminar

---

## Cómo Usar

### Crear Nueva Partida
```
1. Ejecuta: python main.py
2. Selecciona: "Nueva Partida"
3. Sigue el flujo de creación de personaje
4. ¡Explora el mundo!
5. Presiona ESC para guardar y salir
```

### Cargar Partida Guardada
```
1. Ejecuta: python main.py
2. Selecciona: "Cargar Partida"
3. Elige una partida guardada
4. Presiona ENTER
5. ¡Continúa desde donde estabas!
```

### Guardar Partida
```
Automático:   Cada 30 segundos
Manual:       Presiona F5 en cualquier momento
Al Salir:     Presiona ESC (guarda automáticamente)
```

---

## Controles en Exploración

| Tecla       | Acción                           |
|-------------|----------------------------------|
| ↑ W        | Mover arriba                     |
| ↓ S        | Mover abajo                      |
| ← A        | Mover izquierda                  |
| → D        | Mover derecha                    |
| M          | Mapa local detallado (64x64)     |
| L          | Leyenda de terrenos              |
| I          | Información del terreno actual   |
| F5         | Guardar manualmente              |
| ESC        | Guardar y volver al menú         |

---

## Dónde Se Guardan las Partidas

```
e:\jogo\saves\games\
├── tu_nombre_1\
│   └── save.json
├── arion\
│   └── save.json
└── [nombre_personaje]\
    └── save.json
```

Cada partida tiene su propia carpeta con:
- `save.json` - Estado completo de la partida
- Posición del jugador
- Datos del personaje
- Semilla del mundo

---

## Rendimiento Mejorado

### Antes (Sin Optimizaciones)
- ❌ Movimiento lento (lag visible)
- ❌ Ralentización cada ~50ms
- ❌ Sin guardado automático
- ❌ Solo 1 sesión guardada

### Ahora (Con Optimizaciones)
- ✅ Movimiento fluido (0.003ms)
- ✅ Sin lag perceptible
- ✅ Guardado automático cada 30s
- ✅ Múltiples sesiones guardadas

### Pruebas Realizadas

```
✅ Movimiento 20 veces: 0.06ms total
✅ Cambio de región: 0.02ms (con caché)
✅ Guardado: Completado exitosamente
✅ Carga: Partida restaurada correctamente
✅ Lista de sesiones: 1 sesión encontrada
```

---

## Estructura Interna

### Cache de Mapas Locales
El sistema cachea hasta 9 regiones 64x64 en memoria:
- Región actual: Siempre en caché
- Regiones adyacentes: Cachadas cuando se cargan
- Regiones lejanas: Se descartan para ahorrar memoria

**Resultado:** Cambiar entre regiones cargadas toma solo 1ms.

### Guardado JSON
Cada sesión guarda:
```json
{
    "world": {
        "seed": 12345,
        "player_position": {
            "x": 64,
            "y": 64
        }
    },
    "player": {
        "name": "Arion",
        "race": "Human",
        ...
    },
    "session_name": "arion"
}
```

El mundo se regenera automáticamente usando la misma semilla.

---

## Próximas Mejoras (Futuro)

- Compresión de archivos guardados
- Caché en disco de regiones exploradas
- Generación lazy de tiles (solo visibles)
- Múltiples saves por personaje
- Puntos de guardado rápido

---

## Troubleshooting

### "No se guarda mi partida"
- Comprueba que `saves/games/` existe
- Verifica permisos de escritura en la carpeta
- Presiona F5 manualmente y verifica

### "Movimiento aún lento"
- Comprueba que usas Python 3.13+
- Reinicia el juego
- Comprueba CPU/memoria disponible

### "Partida no carga"
- Verifica que el archivo `save.json` existe
- Comprueba que el JSON es válido
- Intenta eliminar y crear nueva partida

---

## Características Técnicas

| Característica            | Especificación          |
|--------------------------|------------------------|
| Tamaño del mundo          | 128x128 tiles           |
| Tamaño del mapa local     | 64x64 tiles             |
| Cache máximo              | 9 regiones (15MB)       |
| Guardado automático       | Cada 30 segundos        |
| Tiempo por movimiento     | 0.003ms (sin lag)       |
| Formato guardado          | JSON (legible)          |
| Reproducibilidad          | 100% (mismo seed)       |

---

## Tips & Tricks

1. **Exploración Eficiente**
   - El mapa local (M) es 4x más detallado
   - Úsalo para planificar rutas

2. **Guardar Rápido**
   - Presiona F5 en cualquier momento
   - No afecta el gameplay

3. **Múltiples Personajes**
   - Crea varios personajes
   - Cada uno tiene su propia carpeta
   - Alterna entre ellos sin perder progreso

4. **Respaldo Manual**
   - Copia la carpeta `saves/games/[nombre]/` a otro lugar
   - Recupera fácilmente si algo falla

---

¡Disfruta de tu aventura sin ralentizaciones y con tu progreso siempre guardado! 🎮
