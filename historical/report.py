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
Reports on histories.
"""

from historical.burndown import create_burndown_html
from report.enhanced_html import HEADER, FOOTER

def dump_node(indent, node, history, level, args):
    """@return a description of the given node."""
    result = ""
    if level >= args.levels:
        return result
    result += "%s %s : %s %s\n" % (
        ' ' * indent, node.tag, node.format_distribution(), node.data)
    result += "<br clear=all/>"
    result += create_burndown_html(history, node) + "\n"
    result += "<br clear=all/>"
    for child in node.children:
        result += dump_node(indent + 2, child, history, level + 1, args)
    return result


def structure_dump_with_history(root, history, args):
    """Write out the whole node @p root with its estimates in a vaguely
    human-readable form."""
    return HEADER + dump_node(0, root, history, 0, args) + FOOTER
