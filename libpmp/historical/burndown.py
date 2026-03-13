"""Utility to create a burndown chart from a task history."""

from io import BytesIO

from matplotlib import pyplot as plt

from libpmp.distributions import distribution
from libpmp.distributions.operations import dist_add


def create_burndown_html(history, node):
    """Create a burndown plot for the given @p node.
    @return that plot as an html `div` element."""
    return ('<div>' +
            create_burndown_svg(history, node) + "</div>")


def create_burndown_svg(history, node):
    """Create a burndown plot for the given @p node.
    @return that plot as a utf-8 string of svg data."""
    plt.clf()
    _plot_burndown(history, node)
    figure_bytes = BytesIO()
    plt.savefig(figure_bytes, format="svg")
    return figure_bytes.getvalue().decode("utf-8")


def _get_historical_costs(history, node):
    """Return a list [(date, distribution)] for a node.

    Totals the projected cost of every predecessor of @p node at every date
    in @p history.
    """
    node_history = history.get_linear_history(node)
    cost_history = []
    for (date, nodes) in node_history:
        cost_for_date = distribution.ZERO
        for node in nodes:
            cost_for_date = dist_add(cost_for_date, node.final_cost())
        cost_history += [(date, cost_for_date)]
    return cost_history


def _burndown_axes(history, node):
    """Configure the axes of the current plot and @return them."""
    axes = plt.axes()
    axes.set_xlabel("Date")
    axes.set_ylabel("Remaining Cost")
    axes.set_title(node.get_display_name())
    axes.set_xlim(left=history.oldest_date(), right=history.most_recent_date())
    axes.set_autoscaley_on(True)
    return axes


def _plot_burndown(history, node):
    """Write a burndown plot to the current pyplot figure."""
    plt.xkcd()  # Represent approximate/unfounded estimates with xkcd art.
    axes = _burndown_axes(history, node)
    costs = _get_historical_costs(history, node)
    dates = [date for (date, _) in costs]

    def quantile_history(q):
        return [cost.quantile(q) for (date, cost) in costs]

    axes.fill_between(dates, quantile_history(0.1), quantile_history(0.9),
                      hatch="/", edgecolor="red")
    axes.fill_between(dates, quantile_history(0.25), quantile_history(0.75),
                      hatch="\\", edgecolor="red")
    axes.plot(dates, quantile_history(0.5), color="black")
    axes.set_ylim(bottom=0.)
