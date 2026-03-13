"""Simple report that prints the structure of the parse tree of the model."""


def report(root, _):
    """Write out the whole node @p root in parser pretty-print form."""
    root.pretty_print()
