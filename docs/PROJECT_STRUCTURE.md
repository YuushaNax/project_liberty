# ESTRUCTURA DEL PROYECTO - Project Liberty v1.3.0

## 📁 Árbol Completo de Carpetas y Archivos

```
e:\jogo\
│
├── 📄 PUNTO DE ENTRADA
│   ├── main.py                           # Inicializador principal
│   ├── config.txt                        # Configuración del juego
│   ├── CHANGELOG.md                      # Historial de versiones (OFICIAL)
│   └── VERSION_HISTORY.md                # Detalles de versionaje
│
├── 📂 docs/                             # DOCUMENTACIÓN CENTRALIZADA
│   ├── README.md                        # Índice de documentación
│   ├── CHANGELOG.md                     # Historial (copia en docs/)
│   ├── ARQUITECTURA_PERSISTENCIA.md     # Diseño técnico del sistema
│   ├── BUGFIX_CARGA_PARTIDAS.md        # Detalles de correcciones
│   ├── BUGFIX_SUMMARY.txt              # Resumen de bugs
│   ├── CONTROLES_MEJORADOS.md          # Sistema de entrada
│   ├── GUIA_COMPLETA.md                # Manual completo
│   ├── GUIA_EXPLORACION.md             # Guía de exploración
│   ├── GUIA_PRUEBAS.md                 # Cómo ejecutar tests
│   ├── GUIA_RAPIDA.md                  # Referencia rápida
│   ├── MEJORAS_GENERACION.md           # Generador mejorado
│   ├── NUEVAS_CARACTERISTICAS.md       # Features de v1.3.0
│   ├── PERSISTENCIA_OPTIMIZACION.md    # Sistema persistencia
│   ├── REFERENCIA_RAPIDA.md            # Quick reference
│   ├── REFERENCIA_RAPIDA.txt           # Quick reference (txt)
│   ├── RESUMEN_FINAL.md                # Conclusiones
│   ├── RESUMEN_TRABAJO.md              # Trabajo realizado
│   └── RESUMEN_VISUAL.txt              # Cambios visuales
│
├── 📂 engine/                          # NÚCLEO DEL JUEGO
│   ├── __init__.py
│   │
│   ├── 📂 world/                       # Sistema de mundo (MEJORADO v1.3.0)
│   │   ├── __init__.py
│   │   ├── world.py                   # ✨ CORE: Persistencia + Caché
│   │   │                              # Líneas: +234 / -12
│   │   │                              # Changes:
│   │   │                              #  - Session management
│   │   │                              #  - Regional cache system
│   │   │                              #  - Optimized movement (0.003ms)
│   │   │                              #  - Save/load mechanism
│   │   ├── generator.py               # Generador procedural
│   │   ├── map_generator.py           # Generador de mapas
│   │   └── __pycache__/
│   │
│   ├── 📂 entities/                   # Entidades del mundo
│   │   ├── __init__.py
│   │   ├── entity.py                  # Clase base Entity
│   │   ├── player.py                  # Clase Player
│   │   ├── npc.py                     # Clase NPC
│   │   └── __pycache__/
│   │
│   ├── 📂 systems/                    # Sistemas de juego
│   │   ├── __init__.py
│   │   ├── combat.py                  # Sistema de combate
│   │   └── __pycache__/
│   │
│   ├── 📂 utils/                      # Utilidades
│   │   ├── __init__.py
│   │   ├── name_generator.py          # Generador de nombres
│   │   └── __pycache__/
│   │
│   └── __pycache__/
│
├── 📂 interface/                      # INTERFAZ DE USUARIO (MEJORADA v1.3.0)
│   ├── __init__.py
│   ├── ui.py                          # UI principal (encoding fix)
│   │
│   ├── 📂 screens/                    # Pantallas (MEJORADAS)
│   │   ├── __init__.py
│   │   ├── base_screen.py             # Clase base para pantallas
│   │   │
│   │   ├── main_menu.py               # Menú principal
│   │   │
│   │   ├── create_player.py           # ✨ Creación de personaje
│   │   │                              # Changes:
│   │   │                              #  - Session name support
│   │   │                              #  - Integration with new system
│   │   │
│   │   ├── load_player.py             # ✨ NUEVA: Cargador de sesiones
│   │   │                              # Features:
│   │   │                              #  - Browse saved games
│   │   │                              #  - Delete functionality
│   │   │                              #  - Position display
│   │   │
│   │   ├── exploration.py             # ✨ CORE: Exploración del mundo
│   │   │                              # Líneas: +120 / -45
│   │   │                              # Changes:
│   │   │                              #  - Dual maps (Global 128x128 + Local 64x64)
│   │   │                              #  - Battle Brothers style visualization
│   │   │                              #  - K_F5 fix (pygame key bug)
│   │   │                              #  - Dynamic UI headers
│   │   │                              #  - Region highlighting
│   │   │
│   │   ├── player_info.py             # Información del personaje
│   │   ├── text_input.py              # Input de texto
│   │   │
│   │   └── __pycache__/
│   │
│   └── __pycache__/
│
├── 📂 saves/                          # PERSISTENCIA (NUEVO SISTEMA v1.3.0)
│   ├── __init__.py
│   │
│   ├── 📂 games/                      # Sesiones guardadas
│   │   ├── 📂 kjkhbg/                 # Sesión 1
│   │   │   └── save.json              # Datos guardados
│   │   │
│   │   ├── 📂 test_character/         # Sesión 2
│   │   │   └── save.json              # Datos guardados
│   │   │
│   │   └── [más sesiones...]          # Cada personaje crea carpeta
│   │
│   └── __pycache__/
│
├── 📂 tests/                          # SUITE DE TESTS (v1.3.0 NUEVO)
│   ├── __init__.py
│   │
│   ├── 📂 persistence/                # ✨ NUEVA CARPETA: Tests persistencia
│   │   ├── README_TESTS.md            # Documentación de tests
│   │   ├── test_persistence.py        # Suite: Persistencia básica
│   │   │                              # 4 casos / 100% passing
│   │   ├── test_load_flow.py          # Suite: Flujo de carga
│   │   │                              # 2 casos / 100% passing
│   │   ├── test_complete_flow.py      # Suite: Flujo completo
│   │   │                              # 7 verificaciones / 100% passing
│   │   └── test_pygame_keys.py        # Suite: Validación de keys
│   │                                   # K_F5 key validation
│   │
│   ├── character_generation_metrics.py   # Test: Generación de personaje
│   ├── examples_advanced_towns.py        # Example: Ciudades avanzadas
│   ├── quick_npc_test.py                 # Test: NPC rápido
│   ├── test_character_creation.py        # Test: Creación personaje
│   ├── test_childhood_events_randomization.py  # Test: Eventos
│   ├── test_name_and_profession.py       # Test: Nombres y profesiones
│   ├── test_npc_generation.py            # Test: Generación NPC
│   ├── test_world_generation.py          # Test: Generación mundo
│   ├── __init__.py
│   │
│   └── __pycache__/
│
├── 📂 assets/                         # RECURSOS (Futuro)
│   ├── images/
│   ├── sounds/
│   └── sprites/
│
├── 📂 data/                           # DATOS DEL JUEGO
│   ├── abilities.json                 # Habilidades
│   ├── childhood_events.json          # Eventos de infancia
│   ├── magic_domain.json              # Dominios mágicos
│   ├── personality_traits.json        # Rasgos de personalidad
│   ├── professions.json               # Profesiones
│   ├── races.json                     # Razas disponibles
│   ├── skills.json                    # Habilidades
│   └── stats.json                     # Estadísticas base
│
└── 📂 .github/                        # CONFIGURACIÓN
    └── copilot-instructions.md        # Instrucciones para Copilot
```

---

## 📊 ESTADÍSTICAS DE ESTRUCTURA

| Categoría | Cantidad | Tamaño Estimado |
|-----------|----------|-----------------|
| Archivos Python | 23 | ~120KB |
| Archivos Documentación | 18 | ~150KB |
| Archivos de Datos | 8 | ~50KB |
| Archivos de Test | 8 | ~45KB |
| Sesiones Guardadas | 2+ | ~3KB c/u |
| **TOTAL** | **59+** | **~368KB** |

---

## 🎯 DIRECTORIO POR FUNCIÓN

### Para JUGADORES
```
Consultar:
├── docs/GUIA_RAPIDA.md         → Cómo jugar
├── docs/GUIA_EXPLORACION.md    → Mecánicas de exploración
└── main.py                      → Ejecutar juego
```

### Para DESARROLLADORES
```
Consultar:
├── docs/ARQUITECTURA_PERSISTENCIA.md    → Cómo funciona
├── engine/world/world.py                → Código principal
├── CHANGELOG.md                         → Qué cambió
├── VERSION_HISTORY.md                   → Versiones y fechas
└── tests/persistence/                   → Ver tests
```

### Para QA/TESTING
```
Ejecutar:
├── tests/persistence/test_complete_flow.py      → Test principal
├── docs/README_TESTS.md                         → Documentación tests
├── docs/GUIA_PRUEBAS.md                         → Cómo hacer tests
└── CHANGELOG.md (criterios de aceptación)       → Validación
```

### Para MANTENER EL PROYECTO
```
Actualizar:
├── CHANGELOG.md                 → Nueva versión
├── VERSION_HISTORY.md           → Timeline
├── docs/README.md               → Índice docs
└── tests/persistence/README_TESTS.md → Nuevos tests
```

---

## 🔄 FLUJO DE ACTUALIZACIÓN

Cuando se agregue nueva versión:

```
1. Modificar código en engine/ o interface/
2. Crear/actualizar tests en tests/persistence/
3. Actualizar CHANGELOG.md (v1.3.0 → v1.4.0)
4. Agregar entrada en VERSION_HISTORY.md
5. Ejecutar test suite completo
6. Mover nueva documentación a docs/
7. Actualizar docs/README.md (índice)
8. Confirmar 100% tests pasando
```

---

## 📈 CRECIMIENTO DEL PROYECTO

### v1.2.0 (Inicial)
```
Archivos: 15
Documentación: Mínima
Tests: 3
Código: ~100 líneas core
```

### v1.3.0 (Actual)
```
Archivos: 59+
Documentación: 18 documentos
Tests: 8 suites
Código: +450 líneas
Organización: COMPLETA
```

### v1.4.0 (Planeado)
```
Archivos: 65+
Documentación: 20+
Tests: 12+ suites
Código: +750 líneas acumuladas
```

---

## 🔐 INTEGRIDAD DE DIRECTORIOS

### Directorios Críticos
```
✅ engine/world/           - Núcleo del juego (BACKUPEAR)
✅ saves/games/            - Datos de usuarios (BACKUPEAR)
✅ docs/                   - Documentación (VERSION CONTROL)
✅ tests/persistence/      - Tests (VERSION CONTROL)
```

### Directorios Seguros de Modificar
```
⚡ interface/screens/      - UI (sin afectar guardado)
⚡ data/                   - Datos de balance
⚡ assets/ (futuro)        - Recursos multimedia
```

### Directorios NO Modificar
```
❌ __pycache__/            - Generado automáticamente
❌ .github/                - Configuración del sistema
```

---

## 📝 CONVENCIONES DE CARPETAS

### Nueva Feature
```
✅ Crear en carpeta lógica (engine/ o interface/)
✅ Agregar tests en tests/persistence/
✅ Documentar en docs/
✅ Actualizar CHANGELOG.md
```

### Nuevo Jugador (Sesión)
```
✅ Se crea automáticamente en saves/games/[nombre]/
✅ Contiene save.json con datos
✅ No requiere intervención manual
```

### Nueva Documentación
```
✅ Crear en docs/
✅ Seguir naming: [TIPO]_[TEMA].md
✅ Agregar en docs/README.md (índice)
```

### Nuevo Test
```
✅ Crear en tests/persistence/
✅ Nombre: test_[feature].py
✅ Documentar en tests/persistence/README_TESTS.md
```

---

**Documento de Referencia**  
**Versión**: 1.3.0  
**Fecha**: 2025-12-03  
**Autor**: GitHub Copilot  
**Status**: ✅ OFICIAL
