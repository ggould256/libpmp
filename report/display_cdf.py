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

"""Simple report that displays a graph of the CDF of the given
distribution."""

from matplotlib import pyplot

from model import node_plot

# Number of samples from distribution to be plotted, pre-interpolation.
NUM_SAMPLES = 100

# Number of interpolated values in plot.
GRAPH_RESOLUTION = 1000


def report(node, args):
    """Generate and display the graph."""
    node_plot.cdf_prep(node, args)
    pyplot.show()
