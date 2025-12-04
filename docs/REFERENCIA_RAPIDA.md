# 🎮 REFERENCIA RÁPIDA - EXPLORACIÓN

## ⚡ INICIO RÁPIDO

```bash
python main.py
# → Nueva Partida → Crear personaje → ¡Explora!
```

## ⌨️ CONTROLES ESENCIALES

```
MOVIMIENTO: W/S/A/D o FLECHAS
LEYENDA:    L
INFO:       I  
SALIR:      ESC
```

## 🗺️ TERRENOS (ASCII)

```
~  Océano (no caminar)
.  Agua poco profunda (no caminar)
s  Arena (caminar)
g  Hierba (caminar)
f  Bosque (caminar)
^  Montaña (caminar)
A  Picos nevados (caminar)
@  Arena de combate (caminar, rara)
#  Grieta profunda (no caminar)
```

## 🌡️ TEMPERATURAS

```
❄️ Congelado/Frío     → Colores azules/grises
🧊 Fresco             → Colores moderados
😐 Templado           → Colores normales
☀️ Cálido             → Colores más brillantes
🔥 Caliente           → Colores rojo-dorados
```

## 🎨 COLORES PRINCIPALES

| Terreno | Frío | Templado | Caliente |
|---------|------|----------|----------|
| **Arena** | (180,160,100) | (210,180,80) | (240,200,60) |
| **Hierba** | (80,120,60) | (100,180,80) | (120,200,60) |
| **Bosque** | (40,80,40) | (60,120,40) | (80,140,50) |
| **Montaña** | (150,150,180) | (140,100,60) | (120,60,20) |

## 📊 INTERFAZ

```
═══════════════════════════════════════════════
TÍTULO: EXPLORACIÓN DEL MUNDO
─────────────────────────────────────────────
Personaje: [Nombre] ([Raza])
Posición: (X, Y) | Terreno: [Tipo] | Temp: [Cat]
─────────────────────────────────────────────
                    [MAPA]
           Tu posición: 🔶
─────────────────────────────────────────────
Terreno: [Nombre]      | Altura: [Valor]
Temperatura: [Categoría] | Temp: [Valor]
Puedes ir a: [direcciones]
Bloqueado: [direcciones]
═══════════════════════════════════════════════
```

## 🚀 FLUJO DE JUEGO

```
Menú Principal
    ↓
Nueva Partida
    ↓
1. Nombre
2. Raza (seleccionar)
3. Edad inicial
4. Eventos de infancia (por edad)
    ↓
Resumen de Personaje
    ↓
EXPLORACIÓN ← ¡NUEVO!
    ├─ Navegar mapa
    ├─ Ver información
    ├─ Presionar ESC para salir
    └─ Volver a menú
```

## 💾 GUARDAR/CARGAR

- ✅ Automático al entrar a exploración
- ✅ Cargar Partida en menú
- ✅ Mundo idéntico cada vez

## 🎯 TIPS RÁPIDOS

1. **L = Leyenda visual** - Usa siempre que necesites referencia
2. **I = Info detallada** - Ver valores exactos
3. **Colores = Temperatura** - Verde oscuro = frío, verde claro = caliente
4. **Panel inferior** - Dice dónde puedes ir
5. **Mapa centrado** - Siempre te ves en el centro
6. **ESC = Volver** - Regresa al menú en cualquier momento

## 🔍 BÚSQUEDA DE ARENAS DE COMBATE

- 🗺️ Busca tiles de **Arena** (s)
- 🌡️ En regiones **Cálidas**
- 💰 ~5% de probabilidad
- 🎯 Puedes cruzarlas como cualquier arena

## 📈 ESTADÍSTICAS TÍPICAS

Mapa 64x64:
- ~60% Tierra (arena, hierba, bosque)
- ~30% Agua (océano, agua poco profunda)
- ~10% Montañas
- ~5% Arenas de combate (en arenas)

## 🎨 PERSONALIZACIÓN POSIBLE

Estos valores están en `exploration.py`:
- `TILE_SIZE = 12` → Tamaño de celda (píxeles)
- `LEGEND_WIDTH = 250` → Ancho de leyenda
- Colores en `FONT_SMALL`, `HIGHLIGHT`, etc.

## 🐛 ERRORES COMUNES

| Error | Solución |
|-------|----------|
| No se mueve | Verificar dirección (panel muestra bloqueados) |
| Leyenda invisible | Presiona L nuevamente |
| Mapa diferente | Normal - basado en nombre del personaje |
| No ve terrenos | Acercarse a ellos (el mapa muestra región local) |

## 📚 ARCHIVOS IMPORTANTES

```
engine/world/
├── map_generator.py      ← Generación del mapa
├── world.py             ← Lógica de navegación
└── __init__.py

interface/screens/
├── exploration.py        ← Pantalla de exploración
├── create_player.py     ← Transición a exploración
└── base_screen.py

GUIA_EXPLORACION.md      ← Documentación completa
NUEVAS_CARACTERISTICAS.md ← Cambios técnicos
```

## 🎮 EJEMPLO DE SESIÓN

```
1. python main.py
2. Selecciona "Nueva Partida"
3. Nombre: "Legolas"
4. Raza: "Elfo"
5. Edad: 200
6. Eventos de infancia: (seleccionar opciones)
7. ¡EXPLORACIÓN!
   - Presiona D para ir derecha
   - Presiona L para ver leyenda
   - Presiona I para info
   - Presiona ESC para salir
```

## 🌟 CARACTERÍSTICAS DESTACADAS

✨ **Sistema de Temperatura** - Afecta visualización  
✨ **Colores Dinámicos** - Diferentes según temperatura  
✨ **Arenas de Combate** - Raras, especiales  
✨ **Validación de Movimiento** - No puedes cruzar agua  
✨ **Información Detallada** - Panel completo de stats  
✨ **Leyenda Interactiva** - Referencia visual  
✨ **Determinístico** - Mismo nombre = mismo mundo  

---

**¡Listo para explorar? ¡Presiona ENTER para comenzar!** 🗺️✨
