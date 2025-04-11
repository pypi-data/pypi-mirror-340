# 🥷 `ninja_import`

`ninja_import` is a low-level dynamic import helper that allows you to **import individual modules and attributes without triggering full package imports**.

It is especially useful when:

- You want to import a deeply nested module *without* loading its parent packages.
- You need to cherry-pick specific attributes from a module dynamically.
- You want to load modules from a specific file system location without adding it to `sys.path`.
- You're writing test frameworks, plugin systems, or CLI tools that inspect external code.

---

## ✨ Key Benefits

- ✅ **Avoids package-level side effects** when importing deeply nested modules
- ✅ Works with standalone files or package `__init__.py`
- ✅ Handles multiple attributes cleanly
- ✅ Respects Python's module cache (`sys.modules`) for performance

---

## 📄 Example Usage

### ▶️ Import a nested module (without importing its parent package)
```python
mod = ninja_import('myproject.plugins.helpers.nested_tool', path='/absolute/path/to/code')
print(mod.__name__)  # => nested_tool
```

### ▶️ Import a single attribute from a nested module
```python
get_data = ninja_import('myproject.plugins.helpers.nested_tool', 'get_data', path='/absolute/path/to/code')
result = get_data()
```

### ▶️ Import multiple attributes
```python
func1, CONST = ninja_import('myproject.plugins.helpers.nested_tool', 'func1 CONST', path='/absolute/path/to/code')
```

---

## 🔍 API Overview

```python
def ninja_import(qualname: str, attr: str | Iterable[str] = '', path: str = '') -> Any:
```

- `qualname`: Fully qualified module name (e.g. `'a.b.c.module'`)
- `attr`: Space-separated string or list of attribute names
- `path`: Optional root directory where the module source is located

**Returns:**
- The module (if `attr` is empty)
- The single attribute (if one attr)
- A list of attributes (if multiple)

**Raises:**
- `ImportError` if module not found
- `AttributeError` if one or more attributes are missing

---

## 🚀 Install

pip install ninja_import

---

## 🧩 Use Cases

- Building test harnesses or CLI tools that load user code
- Writing plugin loaders for tools
- Dynamically inspecting modules in a sandbox
- Avoiding large package overhead just to reach a small submodule

---

## ✅ Tested & Safe

Extensive `pytest` test coverage includes:

- Attribute import from nested packages
- Error reporting for bad modules and attributes
- Submodule isolation without importing parent packages
- Import caching and circular import scenarios

---

## 🌐 License

MIT

---

Made with ❤️ for fast, safe, flexible module loading.

