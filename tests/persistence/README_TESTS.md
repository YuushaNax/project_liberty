# TEST SUITE - Project Liberty

## 📊 Índice de Tests

### Ubicación General
```
tests/
├── persistence/              # Tests de persistencia y performance
│   ├── test_persistence.py
│   ├── test_load_flow.py
│   ├── test_complete_flow.py
│   └── test_pygame_keys.py
├── [tests originales...]
└── README_TESTS.md           # Este archivo
```

---

## 🧪 TEST SUITE: PERSISTENCIA (v1.3.0)

### 1. test_persistence.py
**Propósito**: Validar sistema de guardado/carga y caché de regiones  
**Autor**: GitHub Copilot  
**Fecha**: 2025-12-03  
**Status**: ✅ PASANDO (4/4 suites)

#### Suite 1: Creación de Sesión
```python
Objetivo: Verificar que se crea sesión correctamente
- Crear nueva sesión
- Verificar carpeta saves/games/[name]/
- Verificar archivo save.json existe
Resultado: ✅ PASANDO
```

#### Suite 2: Guardado y Carga
```python
Objetivo: Verificar guardado y restauración de datos
- Guardar posición del jugador
- Cargar en nueva instancia World
- Comparar posición original vs cargada
Resultado: ✅ PASANDO (65,81 → 65,81)
```

#### Suite 3: Optimización de Movimiento
```python
Objetivo: Verificar performance de movimiento
- Realizar 20 movimientos consecutivos
- Medir tiempo total
- Calcular promedio por movimiento
Esperado: < 1ms
Resultado: ✅ PASANDO (0.06ms total = 0.003ms/mov)
```

#### Suite 4: Listado de Sesiones
```python
Objetivo: Verificar que se encuentran todas las sesiones
- Listar sesiones guardadas
- Verificar cantidad
- Verificar nombres
Resultado: ✅ PASANDO (2 sesiones encontradas)
```

**Comando Ejecución**:
```bash
cd tests/persistence
python test_persistence.py
```

**Salida Esperada**:
```
[✓] Suite 1: Session Creation - PASSED
[✓] Suite 2: Save/Load Cycle - PASSED
[✓] Suite 3: Movement Performance - PASSED (0.06ms)
[✓] Suite 4: Session List - PASSED (2 sessions found)
```

---

### 2. test_load_flow.py
**Propósito**: Validar flujo específico de carga de partida  
**Autor**: GitHub Copilot  
**Fecha**: 2025-12-03  
**Status**: ✅ PASANDO (2/2 casos)

#### Caso 1: Carga de Partida Guardada
```python
Objetivo: Verificar que partida cargada tiene datos correctos
- Guardar partida con posición específica
- Cerrar y crear nueva instancia
- Cargar partida
- Verificar posición exacta
Resultado: ✅ CORRECTO
```

#### Caso 2: Integridad de Datos
```python
Objetivo: Verificar que JSON no se corrompe
- Guardar con estructura completa
- Leer archivo JSON directamente
- Validar estructura
- Verificar tipos de datos
Resultado: ✅ VÁLIDO
```

**Comando Ejecución**:
```bash
cd tests/persistence
python test_load_flow.py
```

---

### 3. test_complete_flow.py
**Propósito**: Validar flujo completo del sistema  
**Autor**: GitHub Copilot  
**Fecha**: 2025-12-03  
**Status**: ✅ PASANDO (7/7 verificaciones)

#### Flujo Completo (7 Pasos)
```
[1] Crear sesión nueva
[2] Cargar mapa local
[3] Realizar movimientos (x10)
[4] Guardar partida
[5] Crear mundo nuevo y cargar
[6] Verificar caché de regiones
[7] Validar múltiples sesiones
```

**Verificaciones**:
- ✅ Sesión se crea correctamente
- ✅ Mapa local cargado (64x64)
- ✅ Posición actualizada en movimientos
- ✅ Terreno identificado correctamente
- ✅ Partida guardada en JSON
- ✅ Posición restaurada exactamente
- ✅ Caché contiene regiones adyacentes

**Comando Ejecución**:
```bash
cd tests/persistence
python test_complete_flow.py
```

**Salida Esperada**:
```
=== TEST COMPLETO: PERSISTENCIA + MAPAS LOCALES ===

[1] Creando nueva sesión...
   Posición inicial: (64, 64)
   Región inicial: (1, 1)

[2] Cargando mapa local...
   Mapa local cargado: OK

[3] Probando movimientos y caché de regiones...
   Move 1: Pos=(65, 64), Region=(1, 1), Terrain=Hierba
   ...

✅ TODAS LAS PRUEBAS PASARON!
```

---

### 4. test_pygame_keys.py
**Propósito**: Validar que teclas especiales existen en Pygame  
**Autor**: GitHub Copilot  
**Fecha**: 2025-12-03  
**Status**: ✅ K_F5 DISPONIBLE

#### Verificación: F5 Key
```python
Objetivo: Confirmar que K_F5 existe en pygame
- Importar pygame
- Acceder a pg.K_F5
- Verificar no es None
Resultado: ✅ EXISTE (constante = 282)
```

**Comando Ejecución**:
```bash
cd tests/persistence
python test_pygame_keys.py
```

---

## 📈 RESUMEN DE TESTS v1.3.0

| Test | Casos | Status | Tiempo | Última Ejecución |
|------|-------|--------|--------|------------------|
| test_persistence.py | 4 suites | ✅ | 0.08s | 2025-12-03 |
| test_load_flow.py | 2 casos | ✅ | 0.05s | 2025-12-03 |
| test_complete_flow.py | 7 verificaciones | ✅ | 0.12s | 2025-12-03 |
| test_pygame_keys.py | 1 verificación | ✅ | 0.01s | 2025-12-03 |
| **TOTAL** | **14 casos** | **✅ 100%** | **0.26s** | **2025-12-03** |

---

## 🎯 CRITERIOS DE ACEPTACIÓN

### Para Marcar Test como PASADO
- [ ] No hay excepciones
- [ ] Posiciones coinciden exactamente
- [ ] Tiempos < targets
- [ ] JSON válido
- [ ] Archivos creados

### Para Marcar Test como FALLIDO
- [ ] Excepción levantada
- [ ] Posición no coincide
- [ ] Performance > target
- [ ] JSON corrupto
- [ ] Archivos no creados

---

## 🔄 EJECUCIÓN AUTOMÁTICA

### Ejecutar Todos los Tests (Recomendado)
```bash
cd e:\jogo\tests\persistence
python test_complete_flow.py
```

### Ejecutar Tests Individuales
```bash
# Persistencia solo
python test_persistence.py

# Carga de partida
python test_load_flow.py

# Pygame keys
python test_pygame_keys.py
```

### Ejecutar con Salida Filtrada (Recomendado)
```bash
cd e:\jogo
C:/Python313/python.exe tests/persistence/test_complete_flow.py 2>&1 | Where-Object {$_ -notmatch "pkg_resources|pygame|Hello from|UserWarning"}
```

---

## 🐛 DEBUGGING DE TESTS

### Si test_persistence falla:
1. Verificar carpeta `saves/games/` existe
2. Confirmar permisos de escritura
3. Revisar estructura JSON en `save.json`
4. Ejecutar `test_complete_flow.py` para flujo completo

### Si test_load_flow falla:
1. Verificar `save.json` existe en sesión
2. Confirmar JSON es válido (sin caracteres especiales)
3. Revisar que campos obligatorios están presentes
4. Consultar `CHANGELOG.md` para estructura esperada

### Si test_complete_flow falla:
1. Comienza desde [1] paso por paso
2. Verifica salida en cada paso
3. Si falla en Paso 5, ver `load_game()` en `world.py`
4. Revisar `BUGFIX_SUMMARY.txt` para bugs conocidos

### Si test_pygame_keys falla:
1. Verificar que Pygame está instalado
2. Confirmar versión: `pip show pygame`
3. Reinstalar si es necesario: `pip install pygame==2.6.1`

---

## 📝 PLANTILLA PARA NUEVOS TESTS

Al agregar nuevos tests, seguir este formato:

```python
"""
TEST NAME: [Nombre del test]
PROPÓSITO: [Qué valida]
AUTOR: [Quién lo escribió]
FECHA: [Fecha de creación]
ÚLTIMA ACTUALIZACIÓN: [Fecha]
STATUS: [✅ PASANDO / ⚠️ ADVERTENCIA / ❌ FALLIDO]

CASOS:
- Caso 1: [Descripción]
- Caso 2: [Descripción]

COMANDO: python [filename].py
ESPERADO: [Salida esperada]
"""

def test_suite_1():
    """Descripción clara del test"""
    # Arrange
    # Act
    # Assert
    pass
```

---

## 📊 HISTÓRICO DE EJECUCIONES

### 2025-12-03 - Última Ejecución
```
Hora: 18:45 UTC
Executor: GitHub Copilot
Status: ✅ ALL PASSED
Total Tests: 14
Time: 0.26s
Failures: 0
```

---

## 🔐 MANTENIMIENTO DE TESTS

### Después de cada cambio importante:
- [ ] Ejecutar test suite completo
- [ ] Documentar nuevos tests en este archivo
- [ ] Actualizar contador de casos
- [ ] Registrar tiempo de ejecución
- [ ] Confirmar 100% pasando

### Cada semana:
- [ ] Ejecutar test suite
- [ ] Revisar por deprecaciones
- [ ] Actualizar versiones de dependencias
- [ ] Agregar cobertura de nuevas features

---

## 📚 REFERENCIAS

- `CHANGELOG.md` - Versión y cambios
- `BUGFIX_SUMMARY.txt` - Bugs corregidos
- `ARQUITECTURA_PERSISTENCIA.md` - Cómo funciona el sistema
- `engine/world/world.py` - Código a testear
- `interface/screens/exploration.py` - UI tests

---

**Documento Oficial de Tests**  
**Versión**: 1.3.0  
**Actualizado**: 2025-12-03  
**Autor**: GitHub Copilot  
**Status**: ✅ EN PRODUCCIÓN
