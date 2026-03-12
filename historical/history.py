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
        """Add an entry to the history"""
        self._entries.append(entry)
        self._entries.sort(key=lambda e: e["date"])

    def add_model(self, model, sort_date):
        """Add a model to the history, with the given date."""
        self.add_entry({"model": model, "date": sort_date})

    def entries(self):
        """Get the entries in this history."""
        return self._entries

    def oldest_date(self):
        """Return the date of the first entry in this history."""
        return self._entries[0]["date"]

    def most_recent_date(self):
        """Return the date of the most recent entry in this history."""
        return self._entries[-1]["date"]

    def most_recent_model(self):
        """Return the model of the most recent entry in this history."""
        return self._entries[-1]["model"]

    def predecessors(self, node):
        """Compute the recent history of a node.

        For a @p node compute the nodes in the prior entry that are its
        logical predecessors.  @return (date, [nodes]) for those predecessors,
        where the nodes list may be empty if there are no predecessors, or
        None if there is no prior entry.

        NOTE:  Currently finds only at most one exact predecessor.
        """
        # TODO(ggould) This is a grossly inadequate algorithm.  Some sort of
        # fuzzy or levenshtein approach would be superior.
        def identifier(node):
            return node.node_name or node.display_name

        for i in range(len(self._entries) - 1, 0, -1):
            entry = self._entries[i]
            if entry["model"].has_descendant(node):
                prior_date = self._entries[i - 1]["date"]
                prior_model = self._entries[i - 1]["model"]
                break
        else:
            return None  # Ran out of history without finding a predecessor.
        # TODO(ggould) Find more priors using a fuzzier match.
        prior_node = prior_model.find_descendant(
            lambda n: identifier(n) == identifier(node))
        if prior_node:
            return (prior_date, [prior_node])
        return (prior_date, [])

    def get_linear_history(self, node):
        """Return a list [(date, {node})] for a node.

        Recursively reads out the predecessor tree of @p node at every date in
        this history.  The last entry in the result will be `node`.
        """
        result = []
        working_set = {node}
        working_date = self.most_recent_date()
        while working_set:
            result = [(working_date, working_set)] + result
            new_working_date = None
            new_working_set = set()
            for working_node in working_set:
                predecessors_result = self.predecessors(working_node)
                if predecessors_result is None:
                    break
                prior_date, predecessors = predecessors_result
                new_working_set.update(predecessors)
                if new_working_date:
                    assert new_working_date == prior_date
                new_working_date = prior_date
            working_date = new_working_date
            working_set = new_working_set
        return result


def history_from_md_texts(texts):
    """Make a `History` from a list of markdown text.  For testing purposes."""
    hist = History()
    for (i, text) in enumerate(texts):
        hist.add_model(from_markdown(text), i)
    return hist
