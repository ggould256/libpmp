"""Simple report that prints the structure of the model with an estimates
5-tuple for each node."""


def dump_quantiles(indent, node):
    """Write a 5-tuple description of the distribution of the given @p node
    at the given @p indent level."""
    print(' ' * indent,
          " : ".join("%d" % round(node.final_cost().quantile(q / 100))
                     for q in (10, 25, 50, 75, 90)))


def dump_node(indent, node, level, args):
    """Print a description of the given node."""
    if level >= args.levels:
        return
    print(' ' * indent, node.tag, ':',
          node.format_distribution(),
          node.data)
    dump_quantiles(indent + 1, node)
    for child in node.children:
        dump_node(indent + 2, child, level + 1, args)


def report(root, args):
    """Write out the whole node @p root with its estimates in a vaguely
    human-readable form."""
    dump_node(0, root, 0, args)
    print("TOTAL:")
    dump_quantiles(0, root)
