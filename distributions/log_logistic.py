# Copyright 2016 Grant Gould, 2016
# This software is provided under the MIT license, a copy of which is
# available in the LICENSE file of this project.

from distributions.distribution import Distribution

class LogLogistic(Distribution):
    """Log-logistic distribution.  This distribution empirically fits many
    software projects and has an easy algebraic CDF, PDF, and quantile
    function that allows scipy to do quick and easy curve fitting from
    multipoint estimates."""

    def __init__(self, alpha, beta):
        """Creates a log-logistic distribution of the given parameters.
        See https://en.wikipedia.org/wiki/Log-logistic_distribution for
        definitions of the parameters."""
        self._alpha = alpha
        self._beta = beta

    def pdf(self, x):
        # Use variable names 'x', 'a', and 'b' for comparability to wikipedia.
        a = self._alpha
        b = self._beta
        if x <= 0: return 0
        return ((b / a) * (x / a) ** (b - 1) /
                (1 + (x / a) ** b) ** 2)

    def cdf(self, x):
        # Use variable names 'x', 'a', and 'b' for comparability to wikipedia.
        a = self._alpha
        b = self._beta
        if x <= 0: return 0
        return 1 / (1 + (x / a) ** -b)

    def point_on_curve(self):
        return self._alpha

    def quantile(self, p):
        # Use variable names 'a' and 'b' for comparability to wikipedia.
        a = self._alpha
        b = self._beta
        return a * (p / (1 - p)) ** (1 / b)
