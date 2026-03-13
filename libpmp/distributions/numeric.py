"""Discrete distribution used for nonparametric functions."""

import math

from libpmp.distributions.distribution import Distribution


class NumericDistribution(Distribution):
    """Class representing a discretization of a distribution, which is
    required after certain mathematical operations (eg convolution).

    The distribution consists of a list of PDF values and an offset.  It is
    automatically scaled to the sum of those PDF values to avoid numeric
    error."""

    def __init__(self, values, offset=0):
        """@p values is a list of PDF values P[i] (automatically normalized)
        representing the probability of an outcome between offset+i and
        offset+i+1."""
        self._values = values
        self._offset = int(offset)
        self._scale = 1 / sum(values)
        assert self._scale > 0, (
            "NumericDistribution(%s) had zero scale" % values)
        assert self._scale < float("inf"), (
            "NumericDistribution(%s) had inf scale" % values)

    BEFORE, AFTER = [-3, -2]

    def _bucket(self, x):
        if x < self._offset:
            return self.BEFORE
        try:
            bucket = math.floor(x) - self._offset
        except OverflowError as _:
            return self.AFTER
        if bucket >= len(self._values):
            return self.AFTER
        return bucket

    def pdf(self, x):
        bucket = self._bucket(x)
        if bucket in (self.BEFORE, self.AFTER):
            return 0
        return self._values[bucket] * self._scale

    def cdf(self, x):
        bucket = self._bucket(x)
        if bucket == self.BEFORE:
            return 0
        elif bucket == self.AFTER:
            return 1
        point_in_bucket = x - bucket - self._offset
        return (sum(self._values[:bucket]) +
                (self._values[bucket] * point_in_bucket)) * self._scale

    def point_on_curve(self):
        return self._offset + (len(self._values) / 2)

    # Leave the default quantile() implementation in place because it is
    # probably fast enough.

    def contains_point_masses(self):
        return False

    def __repr__(self):
        return "NumericDistribution(offset=%d, scale=%f, %s)" % (
            self._offset, self._scale, self._values)
