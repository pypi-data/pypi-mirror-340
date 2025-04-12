# module_inspector/inspector.py
import sys
import types
import json


def extract_imported_packages(as_json=False):
    """
    Analyze the current global namespace and list imported packages, aliases, and sub-modules.

    This function inspects the global namespace (`__main__.__dict__`) and extracts information
    about imported packages, their aliases (if any), and specific objects imported using
    `from ... import ...` statements. It excludes built-in modules and special names.

    Classification:
      - Direct imports (e.g., `import numpy`) → "numpy"
      - Aliased imports (e.g., `import pandas as pd`) → "pandas (alias: pd)"
      - From-imports (e.g., `from matplotlib.pyplot import plot`) → "matplotlib (members: plot)"

    Args:
        as_json (bool, optional): If True, return the results as a JSON string. Defaults to False.

    Returns:
        list[dict] or str: A list of dictionaries with keys ("module", "alias", "members"),
                           or a JSON string if `as_json` is True.

    Example:
        >>> import numpy as np
        >>> from matplotlib.pyplot import plot
        >>> extract_imported_packages()
        [{'module': 'matplotlib', 'alias': None, 'members': ['plot']},
         {'module': 'numpy', 'alias': 'np', 'members': []}]
    """
    try:
        import __main__

        namespace = __main__.__dict__
    except ImportError:
        namespace = globals()

    builtin_names = set(sys.builtin_module_names)
    EXCLUDED = {"__future__", "__main__"}

    info = {}

    for global_name, value in namespace.items():
        module_name = None
        is_module = False
        if isinstance(value, types.ModuleType):
            module_name = value.__name__
            is_module = True
        elif hasattr(value, "__module__") and value.__module__:
            module_name = value.__module__
            is_module = False
        else:
            continue

        base = module_name.split(".")[0]
        if base in builtin_names or base in EXCLUDED or base.startswith("_"):
            continue

        if base not in info:
            info[base] = {"aliases": set(), "members": set()}

        if is_module:
            if global_name != base:
                info[base]["aliases"].add(global_name)
        else:
            info[base]["members"].add(global_name)

    results = []
    for base in sorted(info.keys()):
        aliases = sorted(info[base]["aliases"])
        members = sorted(info[base]["members"])

        if aliases:
            for alias in aliases:
                results.append(
                    {
                        "module": base,
                        "alias": alias,
                        "members": [],  # alias usage, no members separately tracked
                    }
                )
        else:
            results.append(
                {
                    "module": base,
                    "alias": None,
                    "members": members,
                }
            )

    if as_json:
        return json.dumps(results)
    else:
        return results


if __name__ == "__main__":
    print(extract_imported_packages(as_json=True))
