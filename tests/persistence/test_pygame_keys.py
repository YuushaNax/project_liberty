#!/usr/bin/env python3
import pygame as pg

pg.init()

# Verificar teclas
print("[OK] Verificando atributos de pygame:")
print(f"  K_F5 exists: {hasattr(pg, 'K_F5')}")
print(f"  K_ESCAPE exists: {hasattr(pg, 'K_ESCAPE')}")
print(f"  K_UP exists: {hasattr(pg, 'K_UP')}")
print(f"  K_DOWN exists: {hasattr(pg, 'K_DOWN')}")
print(f"  K_LEFT exists: {hasattr(pg, 'K_LEFT')}")
print(f"  K_RIGHT exists: {hasattr(pg, 'K_RIGHT')}")

# Listar teclas F
print("\nTeclas de función:")
for i in range(1, 13):
    attr = f'K_F{i}'
    exists = hasattr(pg, attr)
    print(f"  {attr}: {exists}")
