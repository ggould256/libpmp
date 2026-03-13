"""
Reports on histories.
"""

from libpmp.historical.burndown import create_burndown_html
from libpmp.report.enhanced_html import FOOTER, HEADER


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
