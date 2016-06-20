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

"""Parse markdown text files."""

import re

import CommonMark
import CommonMark.blocks
import CommonMark.render.renderer

import model.node


ESTIMATE_RE = re.compile('{.*}$')
HEADING_SCALE = 10


class NodeParser(CommonMark.render.renderer.Renderer):
    # The NodeParser will be invoked by CommonMark on entrance and exit to
    # various syntactic elements.  It is flatly syntactic -- entry and exit to
    # headers *both* happen before any of the section text -- with the
    # exception of item(), which is actually recursive.
    #
    # Thus the code below treats item entry and exit as simple tree traversal,
    # while headers are handled quite differently (see header() for details).

    def __init__(self):
        super(NodeParser, self).__init__()
        self.root = model.node.Node()
        self.root.tag = 'root'
        self.root.level = 0
        self.current = self.root

    def _start_child(self, level):
        new_node = model.node.Node()
        new_node.parent = self.current
        new_node.level = level
        self.current.children.append(new_node)
        self.current = new_node

    def _start_sibling(self):
        new_node = model.node.Node()
        new_node.parent = self.current.parent
        new_node.level = self.current.level
        self.current.parent.children.append(new_node)
        self.current = new_node

    def text(self, node, entering=None):
        if "Table of Contents" in node.literal:
            # Special case to avoid double-counting hours in section
            # headers that are duplicated in the ToC.
            return
        self.current.data += node.literal.rstrip()

    def paragraph(self, node, entering):
        # Which text gets an enclosing para and which does not seems obscure,
        # so just treat para ends as node boundaries to be sure of not missing
        # estimates at ends of lines.
        if entering == False and self.current.data:
            self._start_sibling()

    def item(self, node, entering):
        if not entering:
            self.current = self.current.parent
            return

        self._start_child(self.current.parent.level + 0.1)

    def heading(self, node, entering):
        # We must create a node for the heading itself (any text between
        # entering and leaving the heading) and a child for the first text
        # child of the heading (to start absorbing paragraph text).
        #
        # We must make the node tree depths correlate with the heading levels
        # as much as practical, so that the node tree resembles the heading
        # tree.

        if entering:
            if node.level > self.current.level:
                self._start_child(node.level)
            elif node.level == self.current.level:
                self._start_sibling()
            else:
                while ((self.current.parent is not self.root) and
                       (node.level <= self.current.level)):
                    self.current = self.current.parent
                self._start_sibling()
            return
        else:
            if self.current is not self.root:
                self._start_child(node.level + 0.001)


def process_tree(parent_node):
    # Do all children first.

    # TODO josh.pieper: It would be nice to report where in the tree
    # errors occurred.
    for child in parent_node.children:
        process_tree(child)

    # Then look for a distribution in our data.
    possible_data = ESTIMATE_RE.findall(parent_node.data)
    if len(possible_data) > 1:
        raise RuntimeError('multiple estimates found in one block')
    elif len(possible_data) == 1:
        parent_node.distribution = model.node.make_distribution(
            possible_data[0])


def from_markdown(markdown_text):
    parser = CommonMark.blocks.Parser()
    ast = parser.parse(markdown_text)

    np = NodeParser()
    np.render(ast)

    process_tree(np.root)
    return np.root
