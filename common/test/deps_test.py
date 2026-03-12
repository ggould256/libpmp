#! /usr/bin/env python3

# pylint: disable = line-too-long

"""A check of the environment against our requirements.txt file; adapted from
https://stackoverflow.com/questions/16294819/check-if-my-python-has-all-required-packages
"""

from pathlib import Path
import unittest

import pkg_resources


class TestRequirements(unittest.TestCase):
    """Test that all of our named requirements are present."""
    def test_requirements(self):
        """Recursively confirm that requirements are available."""
        # Ref: https://stackoverflow.com/a/45474387/
        requirements = ((Path(__file__).parents[2] / 'python_requirements.txt')
                        .read_text().strip().split('\n'))
        print(requirements)
        requirements = [r.strip() for r in requirements]
        requirements = [r for r in sorted(requirements)
                        if r and not r.startswith('#')]
        for requirement in requirements:
            with self.subTest(requirement=requirement):
                pkg_resources.require(requirement)


if __name__ == '__main__':
    unittest.main()
