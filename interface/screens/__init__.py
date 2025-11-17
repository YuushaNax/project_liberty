import importlib
import pkgutil

__all__ = []

for module_info in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{module_info.name}")
    globals()[module_info.name] = module
    __all__.append(module_info.name)