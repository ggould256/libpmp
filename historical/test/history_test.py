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

"""Tests for `history`."""

import unittest
from historical.history import history_from_md_texts


class HistoryTest(unittest.TestCase):
    """Tests for `history`."""

    BASIC_HISTORY = history_from_md_texts(
        ["Header\n* Item 1 {3-4}\n * Item 2 {5-6}",
         "Header\n* Item 1 {7-8}\n * Item 2 {9-10}",
         ])

    def test_basic(self):
        """Check that history can do any node correlation at all."""
        history = self.BASIC_HISTORY
        test_node = history.entries()[-1]["model"].find_descendant(
            lambda n: n.display_name == "Item 1")
        assert test_node.distribution_text == "{7-8}"
        assert test_node
        (previous_date, predecessors) = history.predecessors(test_node)
        assert previous_date == 0
        assert len(predecessors) == 1
        found = predecessors[0]
        target = history.entries()[0]["model"].find_descendant(
            lambda n: n.display_name == "Item 1")
        assert found == target
        assert found.distribution_text == "{3-4}"

    def test_linear_history(self):
        history = self.BASIC_HISTORY
        test_node = history.entries()[1]["model"].find_descendant(
            lambda n: n.display_name == "Item 1")
        previous_node = history.entries()[0]["model"].find_descendant(
            lambda n: n.display_name == "Item 1")
        linear_history = history.get_linear_history(test_node)
        assert linear_history == [(0, {previous_node}), (1, {test_node})]

if __name__ == '__main__':
    unittest.main()
