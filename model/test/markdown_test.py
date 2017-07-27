#! /usr/bin/env python3

# Copyright 2016 Toyota Research Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for `from_markdown`."""

# Tests can be sloppy about variable names; it's no big deal.
# pylint: disable = invalid-name

import unittest
from model.from_markdown import from_markdown


class MarkdownTest(unittest.TestCase):
    """Tests markdown parsing for a variety of simple examples."""

    BASIC_MD = """\
Heading
 * single bullet {8-40}
"""

    def test_basic(self):
        """Smoke test of the first markdown file I made that gave a
        wrong parse."""
        model = from_markdown(self.BASIC_MD)
        self.assertEqual(model.tag, "root")
        self.assertEqual(len(model.children), 2)
        self.assertEqual(model.children[0].data, "Heading")
        self.assertEqual(model.children[1].data, "single bullet {8-40}")
        cost = model.children[1].cost()
        self.assertAlmostEqual(cost.quantile(0.1), 8, delta=0.01)
        self.assertAlmostEqual(cost.quantile(0.75), 40, delta=0.01)

    TEXT_AND_BULLETS_MD = """\
Text
 * bullet {8-40}
 * bullet {8-40}
"""

    def test_text_and_bullets(self):
        """Check the generated node structure from a bulleted list."""
        model = from_markdown(self.TEXT_AND_BULLETS_MD)
        self.assertEqual(model.tag, "root")
        self.assertEqual(len(model.children), 3)
        self.assertEqual(model.children[0].data, "Text")
        self.assertEqual(model.children[1].data, "bullet {8-40}")
        self.assertEqual(model.children[2].data, "bullet {8-40}")

    HEADERS_AND_ITEMS_MD = """\
Headline
--------

### Subtask

Goals:

 * Urgent bugs:
   * Everything is full of squirrels {4-15}
 * Less urgent bugs:
   * Some things are not full of squid {4-15}

### Subtask 2

No big deal {10-20}
"""

    def test_headers_and_items(self):
        """Check the generated node structure from a bulleted list."""
        model = from_markdown(self.HEADERS_AND_ITEMS_MD)
        model.pretty_print()
        self.assertEqual(model.tag, "root")
        self.assertEqual(len(model.children), 1)
        self.assertEqual(model.children[0].data, "Headline")
        self.assertEqual(model.children[0].children[0].data, "Subtask")
        self.assertEqual(model.children[0].children[0].children[0].data,
                         "Goals:")
        self.assertEqual(model.children[0].children[0].children[1].data,
                         "Urgent bugs:")
        self.assertEqual(model.children[0].children[0].children[2].data,
                         "Less urgent bugs:")

    COMPLEX_HEADERS_MD = """\
H2 at top level
---------------

 * Node 1

### H3

 * Node 2

H1
==

 * Node 3

## H2 under H1

 * Node 4

## Second H2 under H1

Third H2 under H1
-----------------

"""

    def test_complex_headers(self):
        """Check the generated node structure from a bulleted list."""
        model = from_markdown(self.COMPLEX_HEADERS_MD)
        self.assertEqual(model.tag, "root")
        self.assertEqual(len(model.children), 2)  # H2 at top and H1
        h2 = model.children[0]
        self.assertEqual(len(h2.children), 2)  # Node 1 and H3
        h1 = model.children[1]
        self.assertEqual(len(h1.children), 4)  # Node 3 and three H2s


if __name__ == '__main__':
    unittest.main()
