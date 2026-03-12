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


NODENAME_RE = re.compile("{['\"].*['\"]}$")
ESTIMATE_RE = re.compile("{[^'\"].*}$")
HEADING_SCALE = 10


# pylint faults this for superclass instance attributes, because it sucks.
# pylint: disable=too-many-instance-attributes
class MarkdownNode(model.node.Node):
    """Markdown subclass of Node that retains header structure and crosslinks
    to the markdown AST."""

    def __init__(self):
        """Construct a markdown-flavored Node."""
        super().__init__()
        self.level = None  # For header nodes, the header level.
        self.ast = None  # Markdown AST node corresponding to this.
        self.display_name = ""
        self.node_name = None  # To unify the same node across multiple models.
        self.distribution_text = None  # For testing purposes.


class NodeParser(CommonMark.render.renderer.Renderer):
    """Take a parser stream from a markdown file of estimates and turn it into
    a model for estimation.

    This is a simple syntactic parse of everything except headers; headers
    are treated as a hierarchy all their own, with increasing header numbers
    descending and decreasing header numbers rolling back to the next lower
    numbered header upstream."""

    def __init__(self):
        """Construct the parser."""
        super(NodeParser, self).__init__()
        self.root = MarkdownNode()
        self.root.display_name = "Whole Project"
        self.root.tag = 'root'
        self.root.level = 0
        self.parser_diag = "__init__"
        self.current = self.root

    def _start_child(self, level, ast):
        """Create new descendant node from the current node.  @p level is
        the header level, if any, of this node."""
        new_node = MarkdownNode()
        new_node.parent = self.current
        new_node.level = level
        new_node.ast = ast
        self.current.children.append(new_node)
        self.current = new_node

    def _ascend(self):
        """Pop back up one level in the parse tree."""
        assert self.current != self.root
        self.current = self.current.parent

    # During the parse, CommonMark will stream events at us.  These will
    # be structurally balanced enter/exits of a variety of element types
    # interspersed with text content.  We maintain self.current at the
    # currently open structure; enters cause descent, texts cause children,
    # exits cause ascent.

    def document(self, node, _):
        """Make sure our model's root references the AST root."""
        self.root.ast = node

    # pylint: disable = unused-argument
    def text(self, node, entering=None):
        """Create a text child of the current node, except in the special
        cases of tocs (ignored) and headers (text added to header node)."""
        if "Table of Contents" in node.literal:
            # Special case to avoid double-counting hours in section
            # headers that are duplicated in the ToC.
            return
        parent_tag = self.current.tag
        self._start_child(None, node)
        self.current.tag = "text"
        self.current.parser_diag = "text following " + parent_tag
        self.current.data += node.literal
        self._ascend()

    def softbreak(self, node, entering):
        """Process a softbreak as if it were a literal space."""
        node.literal = " "
        self.text(node, entering)

    def paragraph(self, node, entering):
        """Create a paragraph child of the current node."""
        if not entering:
            self._ascend()
            return
        self._start_child(None, node)
        self.current.tag = "para"
        self.current.parser_diag = "entering para"

    def item(self, node, entering):
        """Create an item child of the current node."""
        if not entering:
            self._ascend()
            return
        self._start_child(None, node)
        self.current.tag = "item"
        self.current.parser_diag = "entering item"

    def heading(self, node, entering):
        """Perform the complex header-processing dance; see implementation
        for details."""
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
            return

        def fully_ascended():
            """Return True if the heading under consideration should be a
            child `self.current`."""
            if self.current.is_root():
                return True
            elif self.current.tag == "heading":
                return self.current.level < node.level
            else:
                return False

        while not fully_ascended():
            self._ascend()

        self._start_child(node.level, node)
        self.current.tag = "heading"
        self.current.parser_diag = "Heading level %d" % node.level


def collapse_empty(subtree):
    """There a whole lot of places in markdown that *could* have text but
    don't.  This results in a very sparse model with a whole lot of empty
    nodes.  This method recursively collapses those nodes."""
    # Recursively simplify the child subtrees.
    for child in subtree.children:
        collapse_empty(child)

    # Eliminate any vacuous children.
    subtree.children = [child for child in subtree.children
                        if child.data or child.children]

    # Adopt text children if we have no text, but not at root.
    if not subtree.is_root():
        if not subtree.data:
            data_as_list = []
            while subtree.children and subtree.children[0].tag == "text":
                data_as_list += [subtree.children[0].data]
                subtree.children = subtree.children[1:]
            subtree.data = ''.join(data_as_list)
        if (not subtree.data and subtree.children and
                subtree.children[0].tag == "para"):
            subtree.data += subtree.children[0].data
            subtree.children = subtree.children[1:]


def process_tree(parent_node):
    """Build distributions for all of the nodes in the given subtree."""
    # Do all children first.
    for child in parent_node.children:
        process_tree(child)

    # Grab a nodename if there is one.
    possible_names = NODENAME_RE.findall(parent_node.data)
    if len(possible_names) > 1:
        raise RuntimeError('multiple node names found in one block: ' +
                           str(possible_names))
    if len(possible_names) == 1:
        parent_node.node_name = possible_names[0]

    # Then look for a distribution in our data.
    possible_data = ESTIMATE_RE.findall(parent_node.data)
    if len(possible_data) > 1:
        raise RuntimeError('multiple estimates found in one block: ' +
                           str(possible_data))
    if len(possible_data) == 1:
        parent_node.distribution_text = possible_data[0]
        parent_node.distribution = model.node.make_distribution(
            possible_data[0])

    parent_node.display_name = parent_node.data.split("{")[0].rstrip()


def from_markdown(markdown_text):
    """Parse markdown text into a `model.Node` tree."""
    parser = CommonMark.blocks.Parser()
    ast = parser.parse(markdown_text)

    parser = NodeParser()
    parser.render(ast)

    model_root = parser.root
    collapse_empty(model_root)
    process_tree(model_root)
    return model_root
