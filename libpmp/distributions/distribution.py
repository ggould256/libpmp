"""Abstract class for probability distributions of resources, along with some
very basic utilities for manipulating them."""

# This is an abstract base class; disable the corresponding pylint complaints.
# pylint: disable = invalid-name, unused-argument, no-self-use

import scipy.optimize


class Distribution:
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
        start = 0.0
        end = start

        # First, scan to find our end point.
        while self.cdf(end) <= p:
            end = 2 * end if end != 0 else 1

        # Then do a simple bisect.
        result = scipy.optimize.bisect(
            lambda x: (self.cdf(x) - p),
            start,
            end)
        return result

    def contains_point_masses(self):
        """Tests may be wrong when a pdf contains a Dirac delta point.  Set
        this true if so."""
        return False


class _ZeroDistribution(Distribution):

    def cdf(self, _):
        return 1

    def pdf(self, _):
        return 0

    def point_on_curve(self):
        return 0

    def quantile(self, _):
        return 0

    def contains_point_masses(self):
        return True


ZERO = _ZeroDistribution()
