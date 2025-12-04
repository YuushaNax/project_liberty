# Guía de Uso - Sistema de Exploración

## 🎮 Cómo Jugar

### Crear un Personaje (Existente)
1. Ejecuta `python main.py`
2. Selecciona "Nueva Partida"
3. Sigue el flujo de creación de personaje:
   - Nombre
   - Raza
   - Edad
   - Eventos de infancia
4. Confirma el resumen

### Explorar el Mundo (NUEVO)
Después de crear tu personaje, automáticamente entrarás en la pantalla de exploración.

---

## ⌨️ CONTROLES DE EXPLORACIÓN

| Tecla | Acción |
|-------|--------|
| **W** o **↑** | Mover hacia arriba |
| **S** o **↓** | Mover hacia abajo |
| **A** o **←** | Mover hacia la izquierda |
| **D** o **→** | Mover hacia la derecha |
| **L** | Mostrar/ocultar leyenda |
| **I** | Información detallada del terreno |
| **ESC** | Volver al menú principal |

---

## 🗺️ ENTENDIENDO LA PANTALLA

### Área Superior (Información)
```
Personaje: Aragorn (Humano)
Posición: (15, 15) | Terreno: Arena | Temp: cold
```

### Centro (Mapa)
- Cada cuadrado representa 1 km²
- **🔶 Dorado** = Tu posición
- Los colores indican terreno y temperatura

### Panel Inferior (Detalles)
```
Terreno: Arena
Temperatura: Frío
Altura: 0.02
Temp: -0.15
```

Muestra:
- Puedes ir a: (lista de direcciones caminables)
- Bloqueado por: (lista de terrenos no caminables)

---

## 🌍 TIPOS DE TERRENO

| Símbolo | Terreno | Caminable | Descripción |
|---------|---------|-----------|-------------|
| ~ | Océano | ❌ | Agua profunda, no navegable |
| . | Agua Poco Profunda | ❌ | Agua poco profunda |
| s | Arena | ✅ | Desiertos y playas |
| g | Hierba | ✅ | Praderas y llanuras |
| f | Bosque | ✅ | Áreas boscosas |
| ^ | Montaña | ✅ | Terreno elevado |
| A | Picos Nevados | ✅ | Montañas cubiertas de nieve |
| @ | Arena de Combate | ✅ | Arenas de lucha especiales (raras) |
| # | Grieta Profunda | ❌ | Abismos profundos |

---

## 🌡️ SISTEMA DE TEMPERATURA

La temperatura afecta los colores y características del terreno:

### Categorías
- **❄️ Congelado** (< -50°): Muy frío
- **❄️ Frío** (-50° a -10°): Frío extremo
- **🧊 Fresco** (-10° a +20°): Moderadamente frío
- **😐 Templado** (+20° a +50°): Neutral
- **☀️ Cálido** (+50° a +80°): Caliente
- **🔥 Caliente** (> +80°): Extremadamente caliente

### Efectos Visuales
El mismo tipo de terreno tiene colores diferentes según temperatura:
- Arena en región fría → Gris
- Arena en región caliente → Dorada brillante
- Bosque en región fría → Oscuro
- Bosque en región cálida → Verde tropical claro

---

## 🎨 LEYENDA (Presiona L)

Muestra referencia visual de:
- Todos los terrenos con sus colores
- Categorías de temperatura
- Símbolo ASCII de cada terreno

---

## 📍 MOVIMIENTO Y NAVEGACIÓN

### Movimiento Básico
- Usa WASD o flechas
- Mensaje confirmando movimiento o bloqueando
- Posición actualizada en tiempo real

### Restricciones
No puedes mover a:
- ❌ Océanos (agua profunda)
- ❌ Grietas profundas
- ❌ Fuera del mapa
- ❌ Agua poco profunda

### Exploración Estratégica
- La temperatura indica clima local
- Algunos terrenos solo aparecen en climas específicos
- Las arenas de combate son raras (5% en áreas de arena caliente)

---

## 💾 GUARDAR Y CARGAR

El juego guarda automáticamente:
- Tu posición en el mapa
- La semilla del mundo (determinista)
- Todos tus stats
- Tu historia de infancia

Para cargar:
1. Selecciona "Cargar Partida" en menú principal
2. Aparecerás en la misma posición
3. El mundo se regenera idénticamente

---

## 🎯 CONSEJOS DE EXPLORACIÓN

1. **Aprende los colores:** Cada color tiene significado
2. **Lee la leyenda:** Presiona L para referencia visual
3. **Navega estratégicamente:** Busca terrenos específicos
4. **Observa la temperatura:** Afecta el ecosistema
5. **Mira las direcciones:** El panel muestra qué terrenos rodean
6. **Evita el agua:** No puedes nadar (aún)

---

## 🔍 INFORMACIÓN DETALLADA

Presiona **I** para expandir información:
- Tipo completo de terreno
- Categoría exacta de temperatura
- Altura del terreno
- Valor de temperatura numérico

---

## 🌐 MAPA MUNDIAL VS LOCAL

El sistema tiene dos niveles:

### Mapa Mundial
- **Mostrado en exploración:** Cada celda = 1 km²
- **Tamaño:** Típicamente 64x64
- **Tiempo de generación:** < 1 segundo

### Mapa Local
- **Generado automáticamente** cuando entras a una región
- **Cada celda:** 5 metros
- **Usado para:** Encuentros, combates, detalles

---

## 🎮 MODO FULLSCREEN

El juego detecta tu monitor automáticamente y usa resolución máxima:
- Los controles se adaptan a cualquier resolución
- El mapa se escala proporcionalmente
- La leyenda siempre es legible

---

## 🐛 TROUBLESHOOTING

### Problema: No puedo moverme
- ✅ Verificar que no estés rodeado de agua
- ✅ Presiona L para ver la leyenda
- ✅ Mira el panel inferior: "Bloqueado por:"

### Problema: Leyenda no se ve
- ✅ Presiona L nuevamente
- ✅ Aumenta la resolución de pantalla

### Problema: Mapa se regenera diferente
- ✅ Cada personaje tiene su propio mundo (basado en su nombre)
- ✅ Mismo nombre = mismo mundo

---

## 🚀 PRÓXIMAS CARACTERÍSTICAS PLANEADAS

- [ ] NPCs y ciudades
- [ ] Combate en arenas
- [ ] Misiones y objetivos
- [ ] Inventario y objetos
- [ ] Sistema de viaje rápido
- [ ] Clima dinámico (lluvia, nieve)
- [ ] Efectos de sonido
- [ ] Modo multijugador (posible futuro)

---

## 📞 SOPORTE

Si encuentras algún bug o tienes sugerencias:
1. Verifica que hayas seguido los controles correctamente
2. Reinicia el juego
3. Intenta crear un nuevo personaje
4. Consulta los logs en la consola

---

**¡Que disfrutes tu aventura! 🗺️✨**
