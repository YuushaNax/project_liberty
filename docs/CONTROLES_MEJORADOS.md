# CONTROLES ACTUALIZADOS - EXPLORACIÓN MEJORADA

## ⌨️ CONTROLES COMPLETOS

| Tecla | Acción | Descripción |
|-------|--------|-------------|
| **W** ↑ | Mover arriba | Movimiento norte |
| **S** ↓ | Mover abajo | Movimiento sur |
| **A** ← | Mover izquierda | Movimiento oeste |
| **D** → | Mover derecha | Movimiento este |
| **L** | Leyenda | Mostrar/ocultar leyenda de terrenos |
| **M** | Mapa Local | Mostrar/ocultar mapa local detallado (NUEVO) |
| **I** | Información | Mostrar información detallada del terreno |
| **ESC** | Salir | Volver al menú principal |

---

## 🗺️ DOS MODOS DE VISUALIZACIÓN

### Modo 1: Mapa Mundial (Por defecto)
- **Tecla:** (Presiona ESC para desactivar leyenda/mapa local)
- **Escala:** 1 km por celda
- **Vista:** 128x128 celdas (128 km²)
- **Información:** Panel inferior con detalles
- **Leyenda:** Presiona L para mostrar

### Modo 2: Mapa Local Detallado (NUEVO)
- **Tecla:** M
- **Escala:** 5 metros por celda
- **Vista:** 64x64 celdas (320m x 320m)
- **Detalle:** Detalles que no se ven en mapa mundial
- **Exclusividad:** Desactiva leyenda automáticamente

---

## 🎮 FLUJO DE JUEGO

```
INICIO
  ↓
Personalización de Personaje
  ↓
EXPLORACIÓN DEL MUNDO
  ├─ Mapa Mundial (por defecto)
  │  ├─ WASD/Flechas: Movimiento
  │  ├─ L: Mostrar Leyenda
  │  ├─ M: Cambiar a Mapa Local
  │  └─ I: Info Detallada
  │
  ├─ Mapa Local (Presionando M)
  │  ├─ Visualización detallada 64x64
  │  ├─ Muestra detalles pequeños
  │  └─ M: Volver a Mapa Mundial
  │
  └─ ESC: Salir a Menú
```

---

## 📊 COMPARACIÓN DE VISTAS

### Mapa Mundial
```
Características:
  ✓ Visión amplia (128 km²)
  ✓ Continentes y océanos
  ✓ Distribución de biomas
  ✓ Ideal para navegación general
  ✓ Información contextual en panel

Desventajas:
  ✗ Detalles pequeños no visibles
  ✗ Claros en bosques imperceptibles
  ✗ Islas en lagos no mostradas
```

### Mapa Local Detallado
```
Características:
  ✓ Máximo detalle (320m²)
  ✓ Claros en bosques visibles
  ✓ Islas y formaciones pequeñas
  ✓ Grietas y detalles del terreno
  ✓ Ideal para exploración profunda

Desventajas:
  ✗ Solo ve región actual
  ✗ No muestra contexto general
  ✗ Menos útil para navegación amplia
```

---

## 💡 SUGERENCIAS DE USO

1. **Navegación General:**
   - Usa Mapa Mundial (L para leyenda)
   - WASD para moverte hacia regiones interesantes
   - I para info de terreno actual

2. **Exploración Detallada:**
   - Presiona M para ver detalles locales
   - Observa claros, islas y características
   - Vuelve a M para continuar navegando

3. **Búsqueda Específica:**
   - Busca Arenas en mapa mundial
   - Usa M para confirmar detalles
   - Navega a nuevas regiones

4. **Estrategia:**
   - Usa Leyenda (L) si no reconoces terrenos
   - Info (I) para datos exactos
   - Alterna entre vistas según necesidad

---

## 🎨 PANEL DE INFORMACIÓN

**Siempre visible en Mapa Mundial:**
```
Personaje: [Nombre] ([Raza])
Posición: (X, Y) | Terreno: [Nombre] | Temp: [Categoría]
─────────────────────────────────────────
Terreno: [Nombre]          Altura: [Valor]
Temperatura: [Categoría]   Temp: [Valor]
Puedes ir a: [Direcciones]
Bloqueado por: [Terrenos]
```

**No visible en Mapa Local:**
- Se reemplaza por vista completa de 320m x 320m
- Información contextual en título

---

## 🌡️ CATEGORÍAS DE TEMPERATURA

En panel de información y leyenda:

```
CATEGORÍA      RANGO        EFECTOS VISUALES
────────────────────────────────────────────
Congelado      < -50°       Azul extremo
Frío           -50° a -10°  Azul frío
Fresco         -10° a +20°  Colores apagados
Templado       +20° a +50°  Colores normales
Cálido         +50° a +80°  Colores brillantes
Caliente       > +80°       Rojo-dorado
```

---

## 🗺️ TERRENOS Y SÍMBOLOS

```
SÍMBOLO    TERRENO              CAMINABLE
──────────────────────────────────────────
~          Océano               ✗
.          Agua poco profunda   ✗
s          Arena/Desierto       ✓
g          Hierba/Pradera       ✓
f          Bosque               ✓
^          Montaña              ✓
A          Picos Nevados        ✓
@          Arena de Combate     ✓
#          Grieta Profunda      ✗
```

---

## 🔍 TECLA I (INFORMACIÓN DETALLADA)

Al presionar I, muestra un mensaje con:
```
[Terreno] - Temp: [Categoría]
```

Ejemplos:
- "Bosque - Temp: cold"
- "Arena - Temp: warm"
- "Montaña - Temp: temperate"

Desaparece automáticamente después de 3 segundos.

---

## 📍 TECLA L (LEYENDA)

Muestra panel lateral con:
- Referencia visual de todos los terrenos con colores
- Categorías de temperatura
- Símbolos ASCII

Presiona L nuevamente para cerrar.
Compatible solo con Mapa Mundial.

---

## 🎯 TECLA M (MAPA LOCAL DETALLADO) - NUEVO

Características:
- Cambia a visualización de mapa local 64x64
- Muestra título: "MAPA LOCAL DETALLADO (64x64 - 320m x 320m)"
- Información: "Cada tile representa 5m"
- Indica: "Presiona M para volver al mapa mundial"
- Escala: Cada tile = 5 metros reales

Usos:
- Ver detalles imperceptibles en mapa mundial
- Explorar características pequeñas
- Confirmar presencia de recursos raros
- Estrategia de navegación local

---

## 🎮 EJEMPLO DE SESIÓN

```
1. [MAPA MUNDIAL] Presiono L
   → Ve leyenda de terrenos

2. [LEYENDA] Presiono L
   → Leyenda desaparece

3. [MAPA MUNDIAL] Presiono I
   → "Bosque - Temp: cold"

4. [MAPA MUNDIAL] Presiono M
   → Cambia a MAPA LOCAL DETALLADO

5. [MAPA LOCAL] Ve detalles de 320m x 320m
   → Observa claros y formaciones

6. [MAPA LOCAL] Presiono M
   → Vuelve a MAPA MUNDIAL

7. [MAPA MUNDIAL] Presiono ESC
   → Vuelve al menú
```

---

## ⚠️ NOTAS IMPORTANTES

- **Leyenda y Mapa Local se excluyen:**
  - Al presionar L se desactiva M
  - Al presionar M se desactiva L

- **Movimiento siempre funciona:**
  - WASD/Flechas funcionan en ambos modos
  - Pero solo en Mapa Mundial el jugador se mueve

- **Performance:**
  - Ambas vistas optimizadas para 30 FPS
  - Sin lag en cambios de vista

- **Determinismo:**
  - Mismo nombre = mismo mundo SIEMPRE
  - Mapa local es consistente dentro del mundo

---

## 🚀 RECOMENDACIÓN DE USO

```
Para nuevo jugador:
  1. Presiona L para ver leyenda
  2. Muévete con WASD (explora general)
  3. Presiona I cuando quieras detalle
  4. Presiona M cuando encuentres algo interesante
  5. Alterna según necesidad

Para jugador avanzado:
  1. USA atajos: L para leyenda, M para zoom
  2. Navega eficientemente entre biomas
  3. Busca formaciones especiales en M
  4. Optimiza rutas explorando
```

---

**¡Disfruta explorando tu mundo único y amplio!** 🗺️✨
