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

"""Report that emits an HTML conversion of the model but with header elements
annotated with estimation results.  Only works with Markdown input, as it
relies on abusing the CommonMark renderer to generate the HTML."""


import CommonMark

from model import node_plot

HEADER = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style>
.floating-box {
    align: right;
    float: right;
}
</style>
<html>
"""

FOOTER = """
</body>
</html>
"""


def distribution_text(node, args):
    """Generates HTML text to be inserted after the header block for
    the provided header @p node."""
    svg = node_plot.cdf_svg(node, args, multi=True)
    html = (
        '<div class="floating-box">' +
        svg +
        "</div>")
    return html


def annotate_asts(subtree, args):
    """For the given MarkdownNode tree, annotate the associated AST with
    estimates information."""
    md_ast = subtree.ast
    if md_ast.t == "heading" and subtree.has_cost():
        dist_ast_node = CommonMark.node.Node("html_block", [])
        dist_ast_node.literal = distribution_text(subtree, args)
        md_ast.insert_after(dist_ast_node)
    for child in subtree.children:
        annotate_asts(child, args)


def report(root, args):
    """Renders out the whole node @p root with its estimates as HTML."""
    renderer = CommonMark.HtmlRenderer()
    annotate_asts(root, args)
    html = renderer.render(root.ast)
    print(HEADER)
    print(html)
    print(FOOTER)
