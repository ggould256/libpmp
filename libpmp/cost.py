#! /usr/bin/env python3

"""Parse structure text files and emit various reports describing how
much effort or cost would be involved."""

import argparse

import libpmp.report.display_cdf
import libpmp.report.enhanced_html
import libpmp.report.parser_debug
import libpmp.report.structure_dump
from libpmp.model.from_html import from_html
from libpmp.model.from_markdown import from_markdown


def main():
    """Parse command line args, load estimates, and dispatch appropriate
    report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--levels', type=int,
                        help='maximum levels to show', default=2)
    parser.add_argument('--report', type=str, default="structure_dump",
                        help='Report to run.')
    parser.add_argument('input')

    args = parser.parse_args()

    data = open(args.input).read()
    if args.input.endswith('.html'):
        root = from_html(data)
    else:
        root = from_markdown(data)

    if args.report == 'structure_dump':
        libpmp.report.structure_dump.report(root, args)
    elif args.report == 'display_cdf':
        libpmp.report.display_cdf.report(root, args)
    elif args.report == 'parser_debug':
        libpmp.report.parser_debug.report(root, args)
    elif args.report == 'enhanced_html':
        assert hasattr(root, "ast")  # Require the CommonMark AST.
        libpmp.report.enhanced_html.report(root, args)
    else:
        parser.error("Unrecognized report: %d" % args.report)

if __name__ == '__main__':
    main()
