# Copyright 2016 Grant Gould, 2016
# This software is provided under the MIT license, a copy of which is
# available in the LICENSE file of this project.

import scipy

"""Abstract class for probability distributions of resources, along with some
very basic utilities for manipulating them."""

class Distribution(object):
    """Abstract class representing a random variable of some resource."""

    def cdf(self, x):
        """@Returns the cumulative value at @p x (that is, the fraction of
        the distribution that is <= x).  This is the inverse of the quantile
        function below.
        NOTE: CDF MUST BE MONOTONIC INCREASING.
        NOTE: CDF(x) MUST BE ZERO FOR ALL x < 0.
        NOTE: CDF(x) MUST APPROACH 1 AT ITS UPPER LIMIT."""
        return NotImplementedError("Distribution classes must define cdf.")

    def pdf(self, x):
        """@Returns the point value at @p x (that is, the probability-per-hour
        measure at x).  If the distribution is approximated or discretized,
        this may measure the average pdf between x and x+1, or the closest
        reasonable analogue to that.
        NOTE: PDF MUST BE EVERYWHERE NONNEGATIVE.
        NOTE: PDF(x) MUST BE ZERO FOR ALL x < 0.
        NOTE: PDF(x) MUST APPROACH ZERO AT ITS UPPER LIMIT."""
        return NotImplementedError("Distribution classes must define pdf.")

    def point_on_curve(self):
        """@Returns any point of nonzero pdf (t: pdf(t) > 0); used to
        initialize scipy.optimize solvers."""
        return NotImplementedError("Distribution classes must define " +
                                   "point_on_curve")

    def quantile(self, p):
        """@Returns the resource level of probability quantile @p p.  For
        example, quantile(0.2) gives the amount of resource that 20% of the
        distribution consumes; quantile(0.5) gives the median."""
        # Default (slow) implementation; subclasses with closed-form quantile
        # functions should override.
        start = self.point_on_curve()
        assert self.pdf(start) > 0  # Or else scipy will run forever.
        result = scipy.optimize.minimize(
            lambda x: (self.cdf(x) - p) ** 2,
            x0=[start])
        return result[0]
