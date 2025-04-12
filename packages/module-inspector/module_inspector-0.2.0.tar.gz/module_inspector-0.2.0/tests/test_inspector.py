import unittest
import sys
import types
import json
from module_inspector import inspector


class TestInspector(unittest.TestCase):
    def setUp(self):
        # Create fake modules for testing
        self.fake_numpy = types.ModuleType("numpy")
        self.fake_pandas = types.ModuleType("pandas")
        self.fake_plot = types.SimpleNamespace(__module__="matplotlib.pyplot")

        # Inject into a mock namespace
        self.original_main = sys.modules["__main__"]
        self.mock_main = types.ModuleType("__main__")
        self.mock_main.__dict__.update(
            {
                "np": self.fake_numpy,  # alias
                "pandas": self.fake_pandas,  # direct import
                "plot": self.fake_plot,  # from-import
            }
        )
        sys.modules["__main__"] = self.mock_main

    def tearDown(self):
        sys.modules["__main__"] = self.original_main

    def test_extract_imported_packages(self):
        expected = [
            {"module": "matplotlib", "alias": None, "members": ["plot"]},
            {"module": "numpy", "alias": "np", "members": []},
            {"module": "pandas", "alias": None, "members": []},
        ]
        result = inspector.extract_imported_packages()
        self.assertEqual(result, expected)

    def test_extract_imported_packages_json(self):
        expected = json.dumps(
            [
                {"module": "matplotlib", "alias": None, "members": ["plot"]},
                {"module": "numpy", "alias": "np", "members": []},
                {"module": "pandas", "alias": None, "members": []},
            ]
        )
        result = inspector.extract_imported_packages(as_json=True)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
