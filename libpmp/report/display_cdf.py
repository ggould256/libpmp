"""Simple report that displays a graph of the CDF of the given
distribution."""

from matplotlib import pyplot

from libpmp.model import node_plot

# Number of samples from distribution to be plotted, pre-interpolation.
NUM_SAMPLES = 100

# Number of interpolated values in plot.
GRAPH_RESOLUTION = 1000


def report(node, args):
    """Generate and display the graph."""
    node_plot.multi_cdf_prep(node, args)
    pyplot.show()
