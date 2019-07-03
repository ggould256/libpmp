#! /usr/bin/env python3

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

"""Parse a series of models; emit a document describing their changes over
time.."""

import argparse

from historical.history import history_from_md_texts
from historical.report import structure_dump_with_history

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
