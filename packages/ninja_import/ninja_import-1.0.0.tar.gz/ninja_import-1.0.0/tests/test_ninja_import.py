import contextlib
import os
import sys
import tempfile
import shutil
from typing import Generator
from pathlib import Path

import pytest

from ninja_import import ninja_import

@pytest.fixture(scope='session')
def tmp_package() -> Generator[tuple[str, str], None, None]:
    """Fixture to create a temporary package structure for testing."""
    with make_temp_package_structure() as tps:
        yield tps

def test_ninja_import_variable(tmp_package: tuple[str, str]) -> None:
    """Test ninja_import with a variable."""
    path, pkg_name = tmp_package
    # ic('INTEST')
    var1 = ninja_import(f'{pkg_name}.module1', 'variable1', path=path)
    assert var1 == 'module1_var'
    assert f'{pkg_name}.module1' in sys.modules
    assert pkg_name not in sys.modules

def test_ninja_import_function(tmp_package: tuple[str, str]) -> None:
    """Test ninja_import with a function."""
    path, pkg_name = tmp_package
    func1 = ninja_import(f'{pkg_name}.module1', 'func1', path=path)
    assert callable(func1)
    assert func1() == 'func1_result'

def test_ninja_import_from_subpackage(tmp_package: tuple[str, str]) -> None:
    """Test ninja_import from a subpackage."""
    path, pkg_name = tmp_package
    var2 = ninja_import(f'{pkg_name}.subpkg.module2', 'variable2', path=path)
    assert var2 == 42

def test_ninja_import_class(tmp_package: tuple[str, str]) -> None:
    """Test ninja_import with a class."""
    path, pkg_name = tmp_package
    TestClass = ninja_import(f'{pkg_name}.subpkg.module2', 'TestClass', path=path)
    assert TestClass.method() == 'class_method_result'

def test_ninja_import_nonexistent_module() -> None:
    """Test ninja_import with a nonexistent module."""
    with pytest.raises(ImportError):
        ninja_import('nonexistent_package.nonexistent_module', 'some_attr')

def test_ninja_import_nonexistent_attribute(tmp_package: tuple[str, str]) -> None:
    """Test ninja_import with a nonexistent attribute."""
    path, pkg_name = tmp_package

    with pytest.raises(AttributeError):
        ninja_import(f'{pkg_name}.module1', 'nonexistent_attr', path=path)

def test_ninja_imports_multiple_attributes(tmp_package: tuple[str, str]) -> None:
    """Test ninja_import with multiple attributes."""
    path, pkg_name = tmp_package

    # Import multiple attributes
    results = ninja_import(f'{pkg_name}.module1', 'variable1 func1')
    print(results)
    assert len(results) == 2
    assert results[0] == 'module1_var'
    assert results[1]() == 'func1_result'

def test_ninja_imports_empty_attributes(tmp_package: tuple[str, str]) -> None:
    """Test ninja_import with empty attributes string."""
    path, pkg_name = tmp_package

    # Import with empty attribute string
    result = ninja_import(f'{pkg_name}.module1')
    assert result.__name__ == 'module1'

def test_ninja_imports_merged_attribute(tmp_package: tuple[str, str]) -> None:
    path, pkg_name = tmp_package
    result = ninja_import(f'{pkg_name}.module1', 'variable1')
    assert result == 'module1_var'

def test_ninja_imports_one_invalid_attribute(tmp_package: tuple[str, str]) -> None:
    """Test ninja_import with one valid and one invalid attribute."""
    path, pkg_name = tmp_package

    # Should raise AttributeError for the invalid attribute
    with pytest.raises((AttributeError, ImportError)):
        ninja_import(f'{pkg_name}.module1', 'variable1 nonexistent_attr')

def test_module_path_resolution(tmp_package: tuple[str, str]) -> None:
    """Test that the module path is correctly resolved."""
    path, pkg_name = tmp_package

    # Override __file__ to simulate running from a different location
    fake_file_path = os.path.join(path, 'fake_location', 'fake_module.py')
    os.makedirs(os.path.dirname(fake_file_path), exist_ok=True)
    Path(fake_file_path).touch()

    # Now test with the patched resolution
    with pytest.raises(AttributeError):
        # This should fail because our monkey patch makes all paths resolve to path
        ninja_import(f'{pkg_name}.nonexistent', 'attr', path=path)

def test_caching_behavior(tmp_package: tuple[str, str]) -> None:
    """Test that the module is cached after first import."""
    path, pkg_name = tmp_package

    # First import
    var1 = ninja_import(f'{pkg_name}.module1', 'variable1', path=path)
    assert var1 == 'module1_var'

    # Replace the module in sys.modules to test caching
    original_module = sys.modules[f'{pkg_name}.module1']

    # Create a fake module with different attributes
    class FakeModule:
        variable1 = 'fake_value'

    sys.modules[f'{pkg_name}.module1'] = FakeModule()

    # Second import should use the cached (now fake) module
    var1_again = ninja_import(f'{pkg_name}.module1', 'variable1', path=path)
    assert var1_again == 'fake_value'

    # Restore original module
    sys.modules[f'{pkg_name}.module1'] = original_module

def test_circular_imports_simulation(tmp_package: tuple[str, str]) -> None:
    """Test a simulation of circular imports."""
    path, pkg_name = tmp_package

    # Create modules with circular references
    with open(os.path.join(path, pkg_name, 'circular1.py'), 'w') as f:
        f.write(f"import {pkg_name}.circular2\nvariable1 = 'circular1_var'")

    with open(os.path.join(path, pkg_name, 'circular2.py'), 'w') as f:
        f.write(f"from {pkg_name}.circular1 import variable1\nvariable2 = f'circular2_var uses {{variable1}}'")

    # This would normally fail with standard imports due to circular dependency
    # But our function should be able to cherry pick variable2
    var2 = ninja_import(f'{pkg_name}.circular2', 'variable2', path=path)

    # We haven't fully imported circular1, so this is a partial import
    assert 'circular2_var uses ' in var2

@contextlib.contextmanager
def make_temp_package_structure() -> Generator[tuple[str, str], None, None]:
    """Create a temporary package structure for testing.

    Returns:
        tuple containing the temp directory path and the package name
    """
    temp_dir = tempfile.mkdtemp()
    pkg_name = 'test_pkg'

    try:
        # Create package structure
        os.makedirs(os.path.join(temp_dir, pkg_name, 'subpkg'), exist_ok=True)

        # Create __init__.py files
        Path(os.path.join(temp_dir, pkg_name, '__init__.py')).touch()
        Path(os.path.join(temp_dir, pkg_name, 'subpkg', '__init__.py')).touch()

        # Create test module files
        with open(os.path.join(temp_dir, pkg_name, 'module1.py'), 'w') as f:
            f.write("variable1 = 'module1_var'\ndef func1(): return 'func1_result'")

        with open(os.path.join(temp_dir, pkg_name, 'subpkg', 'module2.py'), 'w') as f:
            f.write(
                "variable2 = 42\nclass TestClass:\n    @staticmethod\n    def method(): return 'class_method_result'"
            )

        # Add temp_dir to sys.path to make the package importable
        original_path = sys.path.copy()
        original_cwd = os.getcwd()
        sys.path.insert(0, temp_dir)
        os.chdir(temp_dir)
        assert os.path.exists(f'{temp_dir}/{pkg_name}/__init__.py')
        # ic(f'{temp_dir}/{pkg_name}/__init__.py')
        assert os.path.exists(f'{temp_dir}/{pkg_name}/module1.py')
        assert os.path.exists(f'{temp_dir}/{pkg_name}/subpkg/__init__.py')
        assert os.path.exists(f'{temp_dir}/{pkg_name}/subpkg/module2.py')

        yield temp_dir, pkg_name

        # Restore sys.path and current working directory
        sys.path = original_path
        os.chdir(original_cwd)

    finally:
        # Remove created modules from sys.modules to avoid interference
        for module_name in list(sys.modules.keys()):
            if module_name.startswith(pkg_name):
                del sys.modules[module_name]

        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    main()
