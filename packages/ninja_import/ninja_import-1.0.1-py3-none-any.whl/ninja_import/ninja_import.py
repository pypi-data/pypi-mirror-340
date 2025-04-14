import sys
import typing as t
from types import ModuleType
from collections.abc import Iterable
import importlib.util

def ninja_import(qualname: str, attr: t.Union[str, Iterable[str]] = '', path: str = '') -> t.Any:
    module = ninja_import_module(qualname, path)
    if not attr: return module
    if isinstance(attr, str): attr = attr.split()
    try:
        results = [getattr(module, a) for a in attr]
        if len(results) == 1: return results[0]
        return results
    except AttributeError as e:
        raise AttributeError(f"module '{qualname}' has no attr(s) '{attr}'") from e

def ninja_import_module(qualname: str, path: str) -> ModuleType:
    if qualname not in sys.modules:
        # module_name = qualname.split('.')[-1]
        # if not path: path = site.getsitepackages()
#
        # path2 = path or Path(__file__).parent.resolve()
        # module_path = Path(path2).parent / f'{qualname.replace(".","/")}.py'
#
        # Check if path exists, if not assume it's a directory with __init__.py
        # if not module_path.exists():
            # module_path = module_path.parent / '__init__.py'
            # if not module_path.exists():
                # raise ImportError(f'Could not find module at {module_path}')
        # spec = importlib.util.spec_from_file_location(module_name, module_path)

        spec = importlib.util.find_spec(qualname)
        if not spec or not hasattr(spec, 'loader') or not spec.loader:
            raise ImportError(f'Failed to create spec for {qualname} at {module_path}')

        loaded_module = importlib.util.module_from_spec(spec)
        sys.modules[qualname] = loaded_module
        spec.loader.exec_module(loaded_module)
    return sys.modules[qualname]
