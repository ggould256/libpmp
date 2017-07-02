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

"""Parse structure text files and emit various reports describing how
much effort or cost would be involved."""

import argparse

from model.from_html import from_html
from model.from_markdown import from_markdown
import report.structure_dump
import report.display_cdf


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
        report.structure_dump.report(root, args)
    elif args.report == 'display_cdf':
        report.display_cdf.report(root, args)
    else:
        parser.error("Unrecognized report: %d" % args.report)

if __name__ == '__main__':
    main()
