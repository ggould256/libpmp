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

"""Methods to generate plots from node distributions."""

from io import BytesIO

from matplotlib import pyplot as plt
from numpy import linspace
from scipy.interpolate import interp1d

from common import text
from distributions import distribution
from distributions.operations import dist_add

# Number of samples from distribution to be plotted, pre-interpolation.
NUM_SAMPLES = 100

# Number of interpolated values in plot.
GRAPH_RESOLUTION = 1000


def bounds_for_plotting(dist):
    """Arbitrarily compute and return a (lower_bound, upper_bound) pair for
    the x axis of a plot of the given distribution."""
    high_x = dist.quantile(0.95)
    margin = high_x / 10
    return 0, high_x + margin


def cdf_prep(node, _):
    """Write a graph of the cdf of @p node to the current pyplot."""
    # pylint: disable = invalid-name
    plt.xkcd()
    cost = node.final_cost()
    (x_min, x_max) = bounds_for_plotting(cost)
    xs = linspace(x_min, x_max, NUM_SAMPLES, endpoint=True)
    ys = [cost.cdf(x) for x in xs]
    cubic_y = interp1d(xs, ys, kind="cubic")
    xs_dense = linspace(x_min, x_max, GRAPH_RESOLUTION, endpoint=True)
    plt.plot(xs_dense, cubic_y(xs_dense), '-')


def cdf_svg(node, args, multi=False):
    """Obtain a byte array representing an svg plot of the CDF of @p node."""
    plt.clf()
    if multi:
        multi_cdf_prep(node, args)
    else:
        cdf_prep(node, args)
    figure_bytes = BytesIO()
    plt.savefig(figure_bytes, format="svg")
    return figure_bytes.getvalue().decode("utf-8")


def multi_cdf_prep(node, _):
    """Plot the CDF of @p node, with subdivisions representing the sequence of
    child nodes.

    NOTE: The subdivision plots, though pretty, are not mathematically
    well-founded: Later plots gain more central-limit-theorem love than
    earlier ones, and so the overall node variance will appear to be
    overattributed to the earlier subtasks and underattributed to the later
    ones.
    """
    # pylint: disable = invalid-name, too-many-locals
    plt.xkcd()
    axes = plt.axes()
    axes.set_xlabel("Cost of \"" + text.pretty_truncate(node.data, 35) + "\"")
    axes.set_ylabel("Likelihood")
    colors = ["red", "blue", "black"]
    hatches = ["/", "\\", "o", "-"]

    total_cost = node.final_cost()
    axes.set_title(" : ".join("%d" % round(node.final_cost().quantile(q / 100))
                              for q in (10, 25, 50, 75, 90)))

    cost_so_far = distribution.ZERO
    (x_min, x_max) = bounds_for_plotting(total_cost)
    xs = linspace(x_min, x_max, NUM_SAMPLES, endpoint=True)
    xs_dense = linspace(x_min, x_max, GRAPH_RESOLUTION, endpoint=True)
    curves = []
    nodes_to_plot = [child for child in node.children if child.has_cost()]
    for to_plot in nodes_to_plot:
        cost_so_far = dist_add(cost_so_far, to_plot.final_cost())
        curves.append(([cost_so_far.cdf(x) for x in xs],
                       text.pretty_truncate(to_plot.get_display_name(), 20)))
    if node.distribution:
        # Direct cost in a node with costly children: Odd but not prohibited.
        curves.append((total_cost,
                       text.pretty_truncate(node.get_display_name(), 20)))
    legend = []
    prior_ys = 1.0
    for (ys, name) in curves:
        cubic_y = interp1d(xs, ys, kind="cubic")
        axes.plot(xs_dense, cubic_y(xs_dense), '-', color=colors[0])
        axes.fill_between(xs, prior_ys, ys,
                          hatch=hatches[0],
                          edgecolor=colors[0], facecolor="white")
        if len(curves) > 1:
            legend.append(name)
        colors = colors[1:] + colors[0:1]
        hatches = hatches[1:] + hatches[0:1]
        prior_ys = ys
    axes.legend(legend)
