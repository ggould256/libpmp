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
from numpy import linspace
from scipy.interpolate import interp1d

"""Number of samples from distribution to be plotted, pre-interpolation."""
NUM_SAMPLES = 100

"""Number of interpolated values in plot."""
GRAPH_RESOLUTION = 1000


def bounds_for_plotting(dist):
    """Arbitrarily compute and return a (lower_bound, upper_bound) pair for
    the x axis of a plot of the given distribution."""
    low_x = dist.quantile(0.01)
    high_x = dist.quantile(0.99)
    assert(high_x > low_x)
    margin = (high_x - low_x) / 10
    return (low_x - margin, high_x + margin)


def report(node, args):
    pyplot.xkcd()
    cost = node.final_cost()
    (x_min, x_max) = bounds_for_plotting(cost)
    xs = linspace(x_min, x_max, NUM_SAMPLES, endpoint=True)
    ys = [cost.cdf(x) for x in xs]
    cubic_y = interp1d(xs, ys, kind="cubic")
    xs_dense = linspace(x_min, x_max, GRAPH_RESOLUTION, endpoint=True)
    pyplot.plot(xs_dense, cubic_y(xs_dense), '-')
    pyplot.show()
