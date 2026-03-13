#! /usr/bin/env python3

"""Parse a series of models; emit a document describing their changes over
time.."""

import argparse

from libpmp.historical.history import history_from_md_texts
from libpmp.historical.report import structure_dump_with_history


def main():
    """Parse command line args, load estimates, and generate a report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--levels', type=int,
                        help='maximum levels to show', default=2)
    parser.add_argument('input_mds', nargs="+")

    args = parser.parse_args()

    md_texts = [open(input_md).read() for input_md in args.input_mds]
    history = history_from_md_texts(md_texts)
    model = history.most_recent_model()
    print(
        structure_dump_with_history(model, history, args)
    )

if __name__ == '__main__':
    main()
