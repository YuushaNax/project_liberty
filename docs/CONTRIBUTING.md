# GUÍA DE CONTRIBUCIÓN - Project Liberty

## Cómo Contribuir al Proyecto

### 📋 Tabla de Contenidos
1. [Antes de Empezar](#antes-de-empezar)
2. [Configuración de Desarrollo](#configuración-de-desarrollo)
3. [Flujo de Trabajo](#flujo-de-trabajo)
4. [Estándares de Código](#estándares-de-código)
5. [Documentación](#documentación)
6. [Versionaje](#versionaje)
7. [Checklist de PR](#checklist-de-pr)

---

## ❗ Antes de Empezar

### Requisitos
- Python 3.13+
- Pygame 2.6.1+
- Git (para version control)
- Familiaridad con el proyecto

### Documentos Obligatorios a Leer
1. `docs/README.md` - Índice de documentación
2. `CHANGELOG.md` - Últimas changes
3. `docs/ARQUITECTURA_PERSISTENCIA.md` - Cómo funciona el sistema
4. `tests/persistence/README_TESTS.md` - Cómo hacer tests

### Verificar Estado Actual
```bash
# Ver versión actual
cat CHANGELOG.md | grep "^\## \[v"

# Ver últimas sesiones
ls saves/games/

# Ejecutar tests
cd tests/persistence
python test_complete_flow.py
```

---

## ⚙️ Configuración de Desarrollo

### 1. Clonar/Descargar Proyecto
```bash
cd e:\
git clone [proyecto-url]
cd jogo
```

### 2. Instalar Dependencias
```bash
pip install pygame==2.6.1
pip install numpy
pip install screeninfo
```

### 3. Verificar Instalación
```bash
python main.py
# O ejecutar tests
python tests/persistence/test_complete_flow.py
```

### 4. Configurar Editor
- **IDE Recomendado**: VS Code
- **Extensión**: Python (Microsoft)
- **Formatting**: Autopep8 o Black
- **Linter**: Pylint

---

## 🔄 Flujo de Trabajo

### Paso 1: Crear Branch para Feature
```bash
git checkout -b feature/tu-feature-name
# O para bugfix:
git checkout -b bugfix/tu-bug-name
```

**Convenciones de Nombres**:
- Features: `feature/save-system`, `feature/combat-v2`
- Bugfixes: `bugfix/k-f5-key`, `bugfix/position-restore`
- Hotfixes: `hotfix/critical-crash`

### Paso 2: Desarrollar Feature
1. Modificar código en carpetas apropiadas
2. Mantener estructura de carpetas
3. Usar convenciones de nombres
4. Comentar código importante

### Paso 3: Crear Tests
```bash
# Nuevo test debe ir en tests/persistence/
# Nombre: test_[feature_name].py

# Contenido mínimo:
"""
TEST NAME: [Nombre]
PROPÓSITO: [Qué valida]
AUTOR: [Tu nombre]
FECHA: [Hoy]
"""

def test_feature_1():
    """Descripción del test"""
    # Arrange
    # Act
    # Assert
    pass
```

### Paso 4: Ejecutar Tests
```bash
# Ver que no rompiste tests existentes
python tests/persistence/test_complete_flow.py

# Ejecutar tu nuevo test
python tests/persistence/test_tu_feature.py

# Verificar 100% pasando
```

### Paso 5: Documentar
1. Agregar comentarios en código
2. Crear/actualizar docs en `docs/`
3. Actualizar `CHANGELOG.md`
4. Actualizar `VERSION_HISTORY.md`

### Paso 6: Commit y Push
```bash
git add [archivos-modificados]
git commit -m "[TIPO] Descripción de cambio - v1.3.0+"
git push origin feature/tu-feature-name
```

**Formato de Commit**:
```
[FEATURE] Agregado sistema X - v1.3.1
[BUGFIX] Corregido bug Y - v1.3.1
[DOCS] Actualizada documentación - v1.3.0
[TEST] Agregado test para feature Z - v1.3.1
[REFACTOR] Mejorado código en module X - v1.3.1
```

### Paso 7: Pull Request
1. Escribir descripción clara
2. Referenciar issues relacionados
3. Mencionar cambios clave
4. Incluir screenshot si aplica

**Plantilla PR**:
```markdown
## Descripción
Qué cambió y por qué

## Tipo de Cambio
- [ ] Bugfix
- [ ] Feature
- [ ] Documentación
- [ ] Refactoring
- [ ] Test

## Testing
- [x] Test X pasando
- [x] Test Y pasando

## Checklist
- [x] Código sigue convenciones
- [x] Documentación actualizada
- [x] No hay breaking changes
- [x] 100% tests pasando
```

---

## 📝 Estándares de Código

### Estilo Python (PEP 8)
```python
# ✅ CORRECTO
def calculate_damage(base_damage, modifier):
    """Calcula daño total."""
    return base_damage + modifier

# ❌ INCORRECTO
def calc_dmg(a,b):
    return a+b

# ✅ CORRECTO - Comentarios claros
# Aplicar modificador de cuerpo completo
modified_damage = base_damage * 1.25

# ❌ INCORRECTO
# mods de cuerpo
```

### Estructura de Clases
```python
class Entity:
    """Clase base para entidades del juego."""
    
    def __init__(self, name, position):
        """Inicializa entidad."""
        self.name = name
        self.position = position
    
    def move(self, direction):
        """Mueve la entidad."""
        pass
```

### Manejo de Errores
```python
# ✅ CORRECTO
try:
    game.load_world()
except FileNotFoundError as e:
    print(f"Error: No se encontró archivo - {e}")
except Exception as e:
    logger.error(f"Error inesperado: {e}")

# ❌ INCORRECTO
try:
    game.load_world()
except:
    print("Error")
```

### Nombres de Variables
```python
# ✅ CORRECTO
player_health = 100
monster_position = (64, 81)
is_alive = True

# ❌ INCORRECTO
ph = 100
mp = (64, 81)
a = True
```

---

## 📚 Documentación

### Dónde Documentar

**1. Código** - Docstrings
```python
def save_game(self):
    """
    Guarda la partida actual en archivo JSON.
    
    Estructura de guardado:
    {
        "seed": int,
        "position": [x, y],
        "player_data": {...}
    }
    
    Returns:
        bool: True si el guardado fue exitoso
        
    Raises:
        IOError: Si no se puede escribir archivo
    """
```

**2. Funciones Complejas** - Comentarios
```python
def load_local_map(self):
    # Calcular región actual (64x64 regions)
    region_x = self.player_world_x // 64
    region_y = self.player_world_y // 64
    
    # Verificar si región está en caché
    if (region_x, region_y) in self.local_map_cache:
        return self.local_map_cache[(region_x, region_y)]
```

**3. Features** - Archivo MD en docs/
```markdown
# NUEVA FEATURE: Sistema de Combate V2

## Descripción
Qué es y para qué sirve

## Cómo Funciona
Explicación técnica

## Uso
Ejemplo de código

## Testing
Cómo validar
```

**4. Cambios** - Actualizar CHANGELOG.md
```markdown
## [v1.4.0] - 2025-12-04 - Tu Nombre

### ✨ Features
- [x] Feature 1
- [x] Feature 2

### 🐛 Bugfixes
- [x] Bug 1
- [x] Bug 2
```

---

## 📌 Versionaje

### Formato de Versión
```
[MAJOR].[MINOR].[PATCH]

- MAJOR: Cambios radicales (rompibles)
- MINOR: Nuevas features (compatibles)
- PATCH: Bugfixes (compatibles)
```

### Reglas de Versionaje
- v1.2.0 → v1.3.0 = Nueva feature importante
- v1.3.0 → v1.3.1 = Bugfix
- v1.3.0 → v2.0.0 = Cambios radicales

### Cómo Actualizar Versión

**1. Crear nueva sección en CHANGELOG.md**
```markdown
## [v1.4.0] - 2025-12-04 - Tu Nombre

### 🎯 Objetivos
- [x] Objetivo 1
- [x] Objetivo 2

### ✨ Features
- Feature 1

### 🐛 Bugfixes
- Bug 1

### 📊 Métricas
...
```

**2. Actualizar VERSION_HISTORY.md**
```markdown
## [v1.4.0]

**Fecha**: 2025-12-04
**Autor**: Tu Nombre
**Status**: 🔄 En Desarrollo / ✅ Completado

### Cambios
- Cambio 1
- Cambio 2
```

**3. Actualizar version en código (si aplica)**
```python
# Algunos proyectos tienen __version__
__version__ = "1.4.0"
```

---

## ✅ Checklist de PR

### Antes de Hacer Commit
- [ ] Código sigue PEP 8
- [ ] Sin caracteres especiales no ASCII
- [ ] Sin imports no usados
- [ ] Sin console.log o print() de debug
- [ ] Comentarios claros y útiles

### Antes de Push
- [ ] Tests locales pasan 100%
- [ ] No hay breaking changes
- [ ] Documentación actualizada
- [ ] CHANGELOG.md tiene entrada
- [ ] No hay conflictos con main

### En el PR
- [ ] Descripción clara
- [ ] Referencias a issues
- [ ] Pruebas incluidas
- [ ] Documentación incluida
- [ ] Checklist completado

### Después de Merge
- [ ] Verificar en main
- [ ] Confirmar tests pasan
- [ ] Actualizar tags de versión
- [ ] Celebrar! 🎉

---

## 🎯 Tipos de Contribución

### 1. Bugfixes
**Tiempo Típico**: 30 min - 2 horas
**Steps**:
1. Reportar bug con detalles
2. Escribir test que reproduzca bug
3. Hacer fix
4. Verificar test pasa
5. Actualizar CHANGELOG.md
6. Submit PR

### 2. Features
**Tiempo Típico**: 2 - 8 horas
**Steps**:
1. Discutir feature en issues
2. Diseñar arquitectura
3. Implementar feature
4. Escribir tests completos
5. Documentar extensamente
6. Submit PR

### 3. Documentación
**Tiempo Típico**: 30 min - 2 horas
**Steps**:
1. Identificar gaps en docs
2. Escribir documentación clara
3. Incluir ejemplos
4. Revisar por otros
5. Submit PR

### 4. Testing
**Tiempo Típico**: 1 - 3 horas
**Steps**:
1. Identificar código sin tests
2. Escribir tests comprehensive
3. Verificar 100% cobertura
4. Documentar tests
5. Submit PR

### 5. Refactoring
**Tiempo Típico**: 2 - 6 horas
**Steps**:
1. Identificar código mejorables
2. Refactorizar
3. Asegurar tests pasan
4. Documentar cambios
5. Submit PR

---

## 🆘 Ayuda y Soporte

### Recursos
- Documentación: `docs/README.md`
- Tests: `tests/persistence/README_TESTS.md`
- Arquitectura: `docs/ARQUITECTURA_PERSISTENCIA.md`
- Changes: `CHANGELOG.md`

### Preguntas Frecuentes

**P: ¿Qué carpeta pongo mi código?**
R: Ver `docs/PROJECT_STRUCTURE.md`

**P: ¿Cómo ejecuto los tests?**
R: Ver `tests/persistence/README_TESTS.py`

**P: ¿Cómo actualizo CHANGELOG.md?**
R: Ver sección "Versionaje" arriba

**P: ¿Qué pasa si rompo tests?**
R: Arreglalo antes de push. Si necesitas ayuda, abre issue.

---

## 📞 Contacto

**Mantendor**: GitHub Copilot
**Email**: [Contacto]
**Discord**: [Link]
**Issues**: GitHub Issues

---

**Última Actualización**: 2025-12-03
**Versión**: 1.0
**Status**: ✅ ACTIVO
