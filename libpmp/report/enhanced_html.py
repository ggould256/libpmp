"""Report that emits an HTML conversion of the model but with header elements
annotated with estimation results.  Only works with Markdown input, as it
relies on abusing the CommonMark renderer to generate the HTML."""


import CommonMark

from libpmp.model import node_plot

HEADER = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style>

body {
    margin: 0 2em;
}

.floating-box {
    float: left;
    margin-bottom: 1em;
}

h1, h2, h3, h4, h5, h6, p, ul, ol {
    clear: both;
}

h1, h2, h3, h4, h5, h6 {
    width: 100%;
}

h1 {
    background-color: #666;
    color: white;
    padding: 0.5em 2.25em;
    margin: 0em -2.25em 1em -2.25em;
}

h2 {
    background-color: #ccc;
    padding: 0.5em 2.25em;
    margin: 0em -2.25em 1em -2.25em;
}

h3 {
    border-top: 2px solid #ccc;
    width: 100%;
    padding: 0.25em 2.25em;
    margin: 0.5em -2.25em;
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
