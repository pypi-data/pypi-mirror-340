# Module Inspector

A simple utility to inspect the currently imported packages, aliases, and members in the Python global namespace.

## Installation

Clone the repository and install it:

```bash
git clone https://github.com/ntluong95/module-inspector.git
cd module-inspector
pip install .
```

## Usage
```python
from module_inspector import inspector

# Inspect imported modules
packages = inspector.extract_imported_packages()
print(packages)

# As JSON
packages_json = inspector.extract_imported_packages(as_json=True)
print(packages_json)
```

## Example Output
```json
[
    {"module": "numpy", "alias": "np", "members": []},
    {"module": "matplotlib", "alias": None, "members": ["plot"]}
]
```