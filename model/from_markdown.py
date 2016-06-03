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


ESTIMATE_RE = re.compile('{[\d-]+}')
HEADING_SCALE = 10


class NodeParser(CommonMark.render.renderer.Renderer):
    def __init__(self):
        super(NodeParser, self).__init__()
        self.root = model.node.Node()
        self.root.tag = 'root'
        self.root.level = 0
        self.current = self.root

    def text(self, node, entering=None):
        self.current.data += node.literal

    def paragraph(self, node, entering):
        if not entering:
            return

        if self.current is not self.root:
            self.current = self.current.parent

        new_node = model.node.Node()
        new_node.parent = self.current
        new_node.level = new_node.parent.level + 1
        self.current.children.append(new_node)
        self.current = new_node

    def heading(self, node, entering):
        level_up = 0
        if not entering:
            level_up = 1

        this_level = node.level * HEADING_SCALE + level_up

        while self.current is not self.root:
            if this_level > self.current.level:
                break
            self.current = self.current.parent

        new_node = model.node.Node()
        new_node.parent = self.current
        new_node.level = this_level

        self.current.children.append(new_node)
        self.current = new_node


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
        parent_node.distribution = model.node.make_distribution(possible_data[0])


def from_markdown(markdown_text):
    parser = CommonMark.blocks.Parser()
    ast = parser.parse(markdown_text)

    np = NodeParser()
    np.render(ast)

    process_tree(np.root)
    return np.root
