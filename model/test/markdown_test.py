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

import unittest
from model.from_markdown import from_markdown


class MarkdownTest(unittest.TestCase):

    def test_basic(self):
        """Smoke test of the first markdown file I made that gave a
        wrong parse."""
        md = "Heading\n * item {8-40}"
        model = from_markdown(md)
        self.assertEqual(model.tag, "root")
        self.assertEqual(len(model.children), 2)
        self.assertEqual(model.children[0].data, "Heading")
        cost = model.children[1].cost()
        self.assertAlmostEqual(cost.quantile(0.1), 8, delta=0.01)
        self.assertAlmostEqual(cost.quantile(0.75), 40, delta=0.01)


if __name__ == '__main__':
    unittest.main()
