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

"""Parse structure text files and emit various reports describing how
much effort or cost would be involved."""


import html.parser
import re

from model import node

# The following tags start a child node.
TAG_NODES = ['h1', 'h2', 'h3', 'h4', 'h5', 'li']


def tag_depth(tag):
    if tag not in TAG_NODES:
        return -1
    return TAG_NODES.index(tag)

ESTIMATE_RE = re.compile('{[\d-]+}')


def get_c_class(attrs):
    classes = dict(attrs).get('class', '').split(' ')
    for this_class in classes:
        if this_class.startswith('c') and len(this_class) == 2:
            return int(this_class[1:])

    return 100


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super(Parser, self).__init__()
        self.root = node.Node()
        self.root.tag = 'root'
        self.current = self.root

    def handle_starttag(self, tag, attrs):
        if tag not in TAG_NODES:
            return

        # See if we need to start a new node or back up.
        index = TAG_NODES.index(tag)
        c_class = get_c_class(attrs)

        while self.current is not self.root:
            if tag == 'li' and self.current.tag == 'li':
                if c_class <= self.current.c_class:
                    self.current = self.current.parent
                    continue
                else:
                    break

            if index <= tag_depth(self.current.tag):
                self.current = self.current.parent
                continue

            break

        new_node = node.Node()
        new_node.parent = self.current
        new_node.tag = tag
        new_node.c_class = c_class

        self.current.children.append(new_node)
        self.current = new_node

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        self.current.data += data


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
        parent_node.distribution = node.make_distribution(possible_data[0])


def from_html(html_text):
    html_parser = Parser()
    html_parser.feed(html_text)
    html_parser.root.data = ''
    root = html_parser.root
    process_tree(root)
    return root
