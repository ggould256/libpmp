# Copyright 2019 Toyota Research Institute
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

"""
For a model that changes over time, a datestamped history of its changes
and mechanisms to track those changes.
"""

from model.from_markdown import from_markdown


class History:
    """A datestamped list of models, and utilities for same.

    This is intended to track the history of a whole model.
    A history entry is a map containing at least the following items:
        - model:   The model.Node root of the model.
        - date:  The date of the model (typically a timestamp).
    Entries may have additional items specific to their source (eg, git sha).
    Entries are sorted oldest-to-newest.
    """

    def __init__(self):
        self._entries = []

    def add_entry(self, entry):
        self._entries.append(entry)
        self._entries.sort(key=lambda e: e["date"])

    def add_model(self, model, sort_date):
        self.add_entry({"model": model, "date": sort_date})

    def entries(self):
        return self._entries

    def most_recent_date(self):
        return self._entries[-1]["date"]

    def predecessors(self, node):
        """Compute the recent history of a node.

        For a @p node compute the nodes in the prior entry that are its
        logical predecessors.

        NOTE:  Currently finds only at most one exact predecessor.
        """
        # TODO(ggould) This is a grossly inadequate algorithm.  Some sort of
        # fuzzy or levenshtein approach would be superior.
        identifier = lambda node: node.node_name or node.display_name
        for i in range(len(self._entries) - 1, 0, -1):
            entry = self._entries[i]
            if entry["model"].has_descendant(node):
                model_with_node = entry["model"]
                prior_model = self._entries[i - 1]["model"]
                break
        else:
            return []  # Ran out of history without finding a predecessor.
        prior_node = prior_model.find_descendant(
            lambda n: identifier(n) == identifier(node))
        if prior_node:
            return [prior_node]
        return []


def history_from_md_texts(texts):
    """Make a `History` from a list of markdown text.  For testing purposes."""
    h = History()
    for (i, f) in enumerate(texts):
        h.add_model(from_markdown(f), i)
    return h
