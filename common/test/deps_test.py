#! /usr/bin/env python3

# Adapted from https://stackoverflow.com/questions/16294819/check-if-my-python-has-all-required-packages

from pathlib import Path
import unittest

import pkg_resources

class TestRequirements(unittest.TestCase):
    def test_requirements(self):
        """Recursively confirm that requirements are available."""
        # Ref: https://stackoverflow.com/a/45474387/
        requirements = ((Path(__file__).parents[1] / 'requirements.in')
                        .read_text().strip().split('\n'))
        requirements = [r.strip() for r in requirements]
        requirements = [r for r in sorted(requirements)
                        if r and not r.startswith('#')]
        for requirement in requirements:
            with self.subTest(requirement=requirement):
                pkg_resources.require(requirement)
