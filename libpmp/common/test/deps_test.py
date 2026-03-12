#! /usr/bin/env python3

# pylint: disable = line-too-long

"""A check of the environment against our pyproject.toml dependencies."""

import unittest
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path

try:  # Python 3.11+
    import tomllib  # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:  # Python 3.10 and earlier
    import tomli as tomllib  # pyright: ignore[reportMissingImports]


class TestRequirements(unittest.TestCase):
    """Test that all of our named requirements are present."""
    def test_requirements(self):
        """Confirm that all dependencies in pyproject.toml are installed."""
        # Read and parse pyproject.toml
        pyproject_path = Path(__file__).parents[3] / 'pyproject.toml'
        with open(pyproject_path, 'rb') as f:
            pyproject_data = tomllib.load(f)

        # Extract dependencies from [project] section
        dependencies = pyproject_data.get('project', {}).get('dependencies', [])

        # Parse each requirement to get the package name
        requirements = []
        for dep in dependencies:
            # Remove version specifiers and extras to get package name
            # e.g., "package>=1.0" -> "package", "package[extra]>=1.0" -> "package"
            package_name = dep.split('[')[0].split(';')[0]
            for op in ('>=', '<=', '==', '!=', '~=', '>', '<'):
                package_name = package_name.split(op)[0]
            package_name = package_name.strip()
            requirements.append((package_name, dep))

        requirements = sorted(set(requirements))

        for package_name, requirement in requirements:
            with self.subTest(requirement=requirement):
                try:
                    distribution(package_name)
                except PackageNotFoundError:
                    self.fail(
                        f"Required package '{package_name}' from requirement "
                        f"'{requirement}' is not installed"
                    )


if __name__ == '__main__':
    unittest.main()
