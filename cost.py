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

'''Parse structure text files and emit various reports describing how
much effort or cost would be involved.'''


import argparse
import html.parser
import re
import scipy.optimize

from distributions.log_logistic import LogLogistic
from distributions.point_distribution import PointDistribution
from distributions import operations


# The following tags start a child node.
TAG_NODES = ['h1', 'h2', 'h3', 'h4', 'h5', 'li']

ESTIMATE_RE = re.compile('{[\d-]+}')


class Node(object):
    def __init__(self):
        self.tag = ''
        self.c_class = 0
        self.parent = None
        self.children = []
        self.data = ''
        self.distribution = None

    def index(self):
        if self.tag not in TAG_NODES:
            return -1
        return TAG_NODES.index(self.tag)

    def format_distribution(self):
        if self.distribution is None:
            return ''

        def fmt(x):
            if x is None:
                return ''
            return '%.0f' % x
        return '(%s,%s,%s)' % tuple(fmt(self.distribution.quantile(p))
                                    for p in [0.1, 0.5, 0.9])


def get_c_class(attrs):
    classes = dict(attrs).get('class', '').split(' ')
    for this_class in classes:
        if this_class.startswith('c') and len(this_class) == 2:
            return int(this_class[1:])

    return 100


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super(Parser, self).__init__()
        self.root = Node()
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
                    
            if index <= self.current.index():
                self.current = self.current.parent
                continue

            break
            
        new_node = Node()
        new_node.parent = self.current
        new_node.tag = tag
        new_node.c_class = c_class
        
        self.current.children.append(new_node)
        self.current = new_node

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        self.current.data += data


def fit_log_logistic(value_10, value_75):
    start = [0.5 * (value_10 + value_75), 1]
    def cdf(x, p):
        return x[0] * (p / (1 - p)) ** (1 / x[1])
        
    result = scipy.optimize.fmin_cg(
        lambda x: ( (cdf(x, 0.1) - value_10) ** 2 +
                    (cdf(x, 0.75) - value_75) ** 2),
        x0=start,
        disp=0)
    return LogLogistic(result[0], result[1])


def make_distribution(data):
    values = data[1:-1].split('-')
    if len(values) == 1:
        return PointDistribution({float(values[0]): 1.0})
        
    # For now, assume always log_logistic if we have a range.
    return fit_log_logistic(float(values[0]), float(values[1]))


def process_tree(node):
    # Do all children first.

    # TODO josh.pieper: It would be nice to report where in the tree
    # errors occurred.
    for child in node.children:
        process_tree(child)

    # Then look for a distribution in our data.
    possible_data = ESTIMATE_RE.findall(node.data)
    if len(possible_data) > 1:
        raise RuntimeError('multiple estimates found in one block')
    elif len(possible_data) == 1:
        node.distribution = make_distribution(possible_data[0])

    # Now roll up any children we may have.
    any_children = False
    for child in node.children:
        
        if child.distribution and node.distribution:
            raise RuntimeError('both child and parent specified data')

        if child.distribution:
            any_children = True

    if any_children:
        for child in node.children:
            if child.distribution is None:
                continue
            elif node.distribution is None:
                node.distribution = child.distribution
            else:
                node.distribution = operations.dist_add(
                    node.distribution, child.distribution)
                print(node.data, 'added child:',
                      child.format_distribution(), child.data)
                print('new distribution:', node.format_distribution())


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('input')
                        
    result = parser.parse_args()

    html_parser = Parser()
    html_parser.feed(open(result.input).read())
    html_parser.root.data = ''

    process_tree(html_parser.root)

    # Print out the tree.

    def dump_node(indent, node):
        print(' ' * indent, node.tag, ':',
              node.format_distribution(),
              node.data)
        for child in node.children:
            dump_node(indent + 2, child)

    dump_node(0, html_parser.root)


if __name__ == '__main__':
    main()
