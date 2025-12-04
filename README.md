# 🎮 PROJECT LIBERTY - Índice Maestro v1.3.0

## Bienvenido a Project Liberty

Este es el documento principal que te guiará a los recursos que necesitas.

---

## 🚀 INICIO RÁPIDO (3 Opciones)

### Opción 1: Quiero Jugar
```
1. Leer: docs/GUIA_RAPIDA.md (5 min)
2. Ejecutar: python main.py
3. Crear nueva partida
4. ¡Divertirse!
```

### Opción 2: Quiero Entender la Arquitectura
```
1. Leer: docs/RESUMEN_EJECUTIVO.md (10 min)
2. Leer: docs/ARQUITECTURA_PERSISTENCIA.md (15 min)
3. Revisar: docs/PROJECT_STRUCTURE.md (10 min)
4. Ver código: engine/world/world.py
```

### Opción 3: Quiero Contribuir
```
1. Leer: docs/CONTRIBUTING.md (20 min)
2. Leer: CHANGELOG.md (10 min)
3. Ver: tests/persistence/README_TESTS.md (10 min)
4. Hacer cambios y submit PR
```

---

## 📚 Navegación por Rol

### 👤 Para Jugadores
**¿Qué necesito saber?**
- Cómo jugar
- Controles
- Dónde guardas
- Cómo cargar

**Documentos**:
1. `docs/GUIA_RAPIDA.md` ← **EMPIEZA AQUÍ**
2. `docs/GUIA_EXPLORACION.md`
3. `docs/REFERENCIA_RAPIDA.md`

**Comando Rápido**:
```bash
python main.py
```

---

### 👨‍💻 Para Desarrolladores
**¿Qué necesito saber?**
- Cómo funciona el código
- Cómo agregar features
- Cómo hacer tests
- Convenciones de proyecto

**Documentos**:
1. `docs/RESUMEN_EJECUTIVO.md` ← **EMPIEZA AQUÍ**
2. `docs/ARQUITECTURA_PERSISTENCIA.md`
3. `docs/PROJECT_STRUCTURE.md`
4. `docs/CONTRIBUTING.md`
5. `CHANGELOG.md`

**Carpetas Importantes**:
- `engine/world/world.py` - Núcleo del sistema
- `interface/screens/exploration.py` - UI principal
- `tests/persistence/` - Tests

---

### 🧪 Para QA/Testing
**¿Qué necesito saber?**
- Cómo ejecutar tests
- Qué testear
- Criterios de aceptación
- Cómo reportar bugs

**Documentos**:
1. `tests/persistence/README_TESTS.md` ← **EMPIEZA AQUÍ**
2. `docs/GUIA_PRUEBAS.md`
3. `CHANGELOG.md` (criterios)
4. `docs/RESUMEN_EJECUTIVO.md`

**Comando Rápido**:
```bash
cd tests/persistence
python test_complete_flow.py
```

---

### 📋 Para Mantendores
**¿Qué necesito saber?**
- Qué cambió y cuándo
- Quién hizo qué
- Historial completo
- Próximas versiones

**Documentos**:
1. `CHANGELOG.md` ← **OFICIAL (EMPIEZA AQUÍ)**
2. `VERSION_HISTORY.md`
3. `docs/README.md` (índice)
4. `docs/PROJECT_STRUCTURE.md`

**Tareas Comunes**:
- Actualizar versión → `CHANGELOG.md`
- Ver historial → `VERSION_HISTORY.md`
- Encontrar doc → `docs/README.md`

---

### 🔍 Para Buscadores de Bugs
**¿Qué necesito saber?**
- Bugs conocidos
- Cómo reportar
- Cómo reproducir
- Historial de fixes

**Documentos**:
1. `docs/BUGFIX_SUMMARY.txt` ← **EMPIEZA AQUÍ**
2. `CHANGELOG.md` (bugs corregidos)
3. `docs/BUGFIX_CARGA_PARTIDAS.md`

**Búsqueda Rápida**:
```bash
Buscar en: CHANGELOG.md
Palabra clave: "Bug" o "BUG"
```

---

## 📁 Índice de Todos los Documentos

### 📌 Archivos en Raíz
```
main.py                  # Punto de entrada del juego
CHANGELOG.md             # Historial oficial de versiones
VERSION_HISTORY.md       # Timeline + autores de cambios
config.txt               # Configuración del juego
```

### 📚 Carpeta docs/ (Documentación Centralizada)
```
README.md                          # Índice de documentación
RESUMEN_EJECUTIVO.md              # Resumen completo (LEER PRIMERO)
PROJECT_STRUCTURE.md              # Estructura del proyecto
CONTRIBUTING.md                   # Guía de contribución

GUIAS:
  GUIA_RAPIDA.md                  # Quick start para jugadores
  GUIA_COMPLETA.md                # Manual completo
  GUIA_EXPLORACION.md             # Cómo explorar
  GUIA_PRUEBAS.md                 # Cómo hacer testing

TÉCNICA:
  ARQUITECTURA_PERSISTENCIA.md    # Diseño del sistema
  NUEVAS_CARACTERISTICAS.md       # Features de v1.3.0
  MEJORAS_GENERACION.md           # Generador mejorado
  CONTROLES_MEJORADOS.md          # Sistema de entrada

REFERENCIAS:
  REFERENCIA_RAPIDA.md            # Cheatsheet
  REFERENCIA_RAPIDA.txt           # Cheatsheet (txt)

RESÚMENES:
  BUGFIX_SUMMARY.txt              # Bugs corregidos
  BUGFIX_CARGA_PARTIDAS.md        # Detalle de bugfixes
  RESUMEN_TRABAJO.md              # Trabajo realizado
  PERSISTENCIA_OPTIMIZACION.md    # Sistema persistencia
  RESUMEN_FINAL.md                # Conclusiones
```

### 🧪 Carpeta tests/persistence/ (Test Suite v1.3.0)
```
README_TESTS.md                   # Documentación de tests
test_persistence.py               # Suite: Persistencia (4 casos)
test_load_flow.py                 # Suite: Flujo de carga (2 casos)
test_complete_flow.py             # Suite: Completo (7 verificaciones)
test_pygame_keys.py               # Suite: Pygame keys (1 caso)
```

### 🎮 Carpeta engine/world/
```
world.py                          # ✨ CORE - Persistencia + Caché
generator.py                      # Generador procedural
map_generator.py                  # Generador de mapas
```

### 🖥️ Carpeta interface/screens/
```
exploration.py                    # ✨ Mapas duales + UI
create_player.py                  # Creación de personaje
load_player.py                    # Cargador de sesiones
main_menu.py                      # Menú principal
```

### 💾 Carpeta saves/games/
```
[personaje_1]/
  save.json                       # Datos guardados
[personaje_2]/
  save.json                       # Datos guardados
```

---

## 🔍 Búsqueda Rápida

### "Necesito encontrar..."

**...cómo jugar**
→ `docs/GUIA_RAPIDA.md`

**...la arquitectura del sistema**
→ `docs/ARQUITECTURA_PERSISTENCIA.md`

**...qué cambió en v1.3.0**
→ `CHANGELOG.md` sección `[v1.3.0]`

**...quién hizo qué**
→ `VERSION_HISTORY.md`

**...bugs conocidos**
→ `docs/BUGFIX_SUMMARY.txt`

**...cómo ejecutar tests**
→ `tests/persistence/README_TESTS.md`

**...cómo contribuir**
→ `docs/CONTRIBUTING.md`

**...la estructura de carpetas**
→ `docs/PROJECT_STRUCTURE.md`

**...la estructura del código**
→ `engine/world/world.py` (line by line)

**...ejemplos de tests**
→ `tests/persistence/test_complete_flow.py`

**...criterios de aceptación**
→ `CHANGELOG.md` sección "Criterios de Aceptación"

**...performance del sistema**
→ `docs/RESUMEN_EJECUTIVO.md` sección "Métricas"

---

## ✅ Checklist de Primer Uso

### Si es Jugador
- [ ] Leer `docs/GUIA_RAPIDA.md`
- [ ] Ejecutar `python main.py`
- [ ] Crear nueva partida
- [ ] Explorar mapas (WASD)
- [ ] Presionar M para mapa local
- [ ] Presionar F5 para guardar
- [ ] Presionar ESC para salir
- [ ] Cargar partida guardada

### Si es Desarrollador
- [ ] Leer `docs/RESUMEN_EJECUTIVO.md`
- [ ] Leer `docs/ARQUITECTURA_PERSISTENCIA.md`
- [ ] Revisar `CHANGELOG.md`
- [ ] Ejecutar `python tests/persistence/test_complete_flow.py`
- [ ] Explorar código en `engine/world/world.py`
- [ ] Leer `docs/CONTRIBUTING.md`
- [ ] Hacer primer cambio
- [ ] Ejecutar tests nuevamente

### Si es QA
- [ ] Leer `tests/persistence/README_TESTS.md`
- [ ] Leer `docs/GUIA_PRUEBAS.md`
- [ ] Ejecutar test suite completo
- [ ] Verificar 100% pasando
- [ ] Jugar game completo
- [ ] Probar guardado/carga
- [ ] Probar mapas locales
- [ ] Documentar hallazgos

### Si es Mantendedor
- [ ] Leer `CHANGELOG.md`
- [ ] Revisar `VERSION_HISTORY.md`
- [ ] Familiarizarse con `docs/` estructura
- [ ] Ver `PROJECT_STRUCTURE.md`
- [ ] Entender versionaje en `docs/CONTRIBUTING.md`
- [ ] Hacer backup de `saves/games/`
- [ ] Estar listo para próxima versión

---

## 🎯 Tareas Comunes

### "Necesito..."

**...jugar el juego**
```bash
python main.py
```

**...ejecutar todos los tests**
```bash
cd tests/persistence
python test_complete_flow.py
```

**...entender el sistema de persistencia**
1. Ver `docs/ARQUITECTURA_PERSISTENCIA.md`
2. Revisar `engine/world/world.py`
3. Ejecutar `tests/persistence/test_persistence.py`

**...agregar una nueva feature**
1. Leer `docs/CONTRIBUTING.md`
2. Ver código relevante en `engine/` o `interface/`
3. Escribir tests
4. Actualizar `CHANGELOG.md`
5. Submit PR

**...reportar un bug**
1. Reproducir en `python main.py`
2. Documentar pasos
3. Ver `docs/BUGFIX_SUMMARY.txt`
4. Crear issue con detalles
5. Referenciar `CHANGELOG.md`

**...actualizar versión**
1. Modificar código
2. Crear tests
3. Agregar sección en `CHANGELOG.md`
4. Agregar entrada en `VERSION_HISTORY.md`
5. Ejecutar test suite (100% debe pasar)

**...encontrar quién hizo qué**
1. Ver `CHANGELOG.md` para cambios por versión
2. Ver `VERSION_HISTORY.md` para timeline
3. Cada cambio tiene autor + fecha

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| Versión Actual | 1.3.0 |
| Status | ✅ Completo |
| Documentos | 18+ |
| Test Cases | 14 |
| Tests Pasando | 14/14 (100%) |
| Bugs Corregidos | 4 |
| Features Nuevas | 4 |
| Performance Mejora | 10,000x |
| Usuarios Simultáneos | ∞ (sesiones independientes) |

---

## 🔗 Links de Referencia Rápida

### Documentos Top 5
1. `docs/RESUMEN_EJECUTIVO.md` - Resumen completo
2. `CHANGELOG.md` - Historial oficial
3. `docs/ARQUITECTURA_PERSISTENCIA.md` - Cómo funciona
4. `tests/persistence/README_TESTS.md` - Tests
5. `docs/CONTRIBUTING.md` - Contribuir

### Código Top 5
1. `engine/world/world.py` - Persistencia + Caché
2. `interface/screens/exploration.py` - UI + Mapas
3. `interface/screens/load_player.py` - Cargador sesiones
4. `tests/persistence/test_complete_flow.py` - Test integral
5. `main.py` - Punto de entrada

### Datos Importantes
1. `saves/games/` - Partidas guardadas
2. `data/` - Datos del juego
3. `config.txt` - Configuración

---

## 🆘 Soporte

**¿No encuentras algo?**
1. Busca en este documento (CTRL+F)
2. Ve a `docs/README.md`
3. Revisa `CHANGELOG.md`
4. Consulta la carpeta específica

**¿Encontraste un bug?**
1. Documenta en `docs/BUGFIX_SUMMARY.txt`
2. Referencia en GitHub Issues
3. Copia el link en `CHANGELOG.md`

**¿Quieres contribuir?**
1. Lee `docs/CONTRIBUTING.md`
2. Sigue el flujo de trabajo
3. Actualiza `CHANGELOG.md`

---

## 📝 Notas Importantes

### Para Todos
> Todo está documentado. Si no encuentras algo, pregunta en Issues.

### Para Desarrolladores
> El código es tuyo para mejorar. Usa las guías. ¡Haz un gran proyecto!

### Para Usuarios
> El juego es estable y listo. ¡Disfruta tu aventura en Project Liberty!

### Para Mantendores
> Cuidado con los cambios. Siempre actualiza CHANGELOG.md + VERSION_HISTORY.md

---

## 🎉 ¡Comienza tu Aventura!

**Eres...**

- 🎮 **Jugador** → Ve a `docs/GUIA_RAPIDA.md` y ejecuta `python main.py`
- 👨‍💻 **Desarrollador** → Ve a `docs/CONTRIBUTING.md` y lee la arquitectura
- 🧪 **QA** → Ve a `tests/persistence/README_TESTS.md` y ejecuta tests
- 📋 **Mantendedor** → Ve a `CHANGELOG.md` y `VERSION_HISTORY.md`

---

**Última Actualización**: 2025-12-03  
**Versión**: 1.3.0  
**Status**: ✅ LISTO PARA PRODUCCIÓN

¡Bienvenido a Project Liberty! 🚀
