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
        self.parser_diag = "__init__"
        self.current = self.root

    def _start_child(self, level):
        new_node = model.node.Node()
        new_node.parent = self.current
        new_node.level = level
        self.current.children.append(new_node)
        self.current = new_node

    def _ascend(self):
        assert self.current != self.root
        self.current = self.current.parent

    # During the parse, CommonMark will stream events at us.  These will
    # be structurally balanced enter/exits of a variety of element types
    # interspersed with text content.  We maintain self.current at the
    # currently open structure; enters cause descent, texts cause children,
    # exits cause ascent.

    def text(self, node, entering=None):
        if "Table of Contents" in node.literal:
            # Special case to avoid double-counting hours in section
            # headers that are duplicated in the ToC.
            return
        if self.current.tag == "heading":
            self.current.parser_diag = "heading text"
            self.current.data += node.literal.rstrip()
        else:
            self._start_child(None)
            self.current.parser_diag = "text"
            self.current.data += node.literal.rstrip()
            self._ascend()

    def paragraph(self, node, entering):
        if not entering:
            self._ascend()
            return
        self._start_child(None)
        self.current.parser_diag = "entering para"

    def item(self, node, entering):
        if not entering:
            self._ascend()
            return
        self._start_child(None)
        self.current.parser_diag = "entering item"

    def heading(self, node, entering):
        # A heading node is a bit odd because heading structure is not
        # reflected in the event stream (the heading node exits immediately
        # at the end of the heading text) but must be in the resulting
        # node stream for our model structure to be right.
        #
        # So when we encounter a heading we first terminate all lesser
        # heading nodes that are open.  This leaves us either at root or at
        # a stronger heading.  We then create a new child and put the heading
        # text into it.
        if not entering:
            self._start_child(node.level)
            return

        def fully_ascended():
            if self.current.is_root():
                return True
            elif self.current.tag == "heading":
                return self.current.level < node.level
            else:
                return False

        while not fully_ascended():
            self._ascend()

        self._start_child(node.level)
        self.current.tag = "heading"
        self.current.parser_diag = "Heading level %d" % node.level


def collapse_empty(subtree):
    """There a whole lot of places in markdown that *could* have text but
    don't.  This results in a very sparse model with a whole lot of empty
    nodes.  This method recursively collapses those nodes.  Returns False
    if the entire subtree passed in is empty."""
    for child in subtree.children:
        collapse_empty(child)
    subtree.children = [child for child in subtree.children
                        if child.data or child.children]
    for (i, child) in enumerate(subtree.children):
        if not child.data and len(child.children) == 1:
            subtree.children[i] = child.children[0]
            subtree.children[i].parent = subtree


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

    model = np.root
    collapse_empty(model)
    process_tree(model)
    return model
