# Copyright 2016 Grant Gould
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

"""Operations on distributions.

NOTE:  These are intentionally not implemented as operations on Distribution,
because operator overloading should be at the model layer, not the
distribution layer (eg, to ensure you can't multiply dollars by dollars) and
so not implementing operators here ensures errors if someone interchanges
distribution and model objects.
"""

import math

from distributions.distribution import Distribution, ZERO
from distributions.numeric import NumericDistribution


_ADD_RESOLUTION = 100


# pylint: disable = invalid-name, too-many-locals
def dist_add(l, r, epsilon=0.01):
    """Returns the sum of random variables distributed by @p l and @p r.  The
    sum of random variables has a pdf that is the convolution of the pdfs of
    the addends."""
    # We will do this by converting the distributions to numeric and then
    # convolving numerically.  Because NumericDistribution takes care of
    # normalization, we ignore numeric error.
    #
    # Discretized convolution is slightly subtle:  The delta in CDF across a
    # given interval in l and r contributes to twice as wide an interval of
    # the result pdf (that is, dCDF[l](0..1) + dCDF[r](0..1) contribute to
    # pdf(0..2)).

    if l == ZERO:
        return r
    if r == ZERO:
        return l

    # First, find the domains where the addends' CDFs are >= epsilon and use
    # that to determine the domain of the result (y).
    l_min = int(math.floor(l.quantile(epsilon)))
    l_max = int(math.ceil(l.quantile(1 - epsilon)))
    r_min = int(math.floor(r.quantile(epsilon)))
    r_max = int(math.ceil(r.quantile(1 - epsilon)))
    y_min = l_min + r_min
    y_max = l_max + r_max
    y_width = y_max - y_min
    y_values = [0] * (y_width + 2)

    l_step = max(1, int((l_max - l_min) / _ADD_RESOLUTION))
    r_step = max(1, int((r_max - r_min) / _ADD_RESOLUTION))

    # Compute the added distribution by repeatedly adding in shifted copies
    # of r, counting on NumericDistribution's normalization to pick up the
    # pieces afterward.
    for x_l in range(l_min, l_max + 1, l_step):
        x_l_prob = l.cdf(x_l + 1) - l.cdf(x_l)
        for x_r in range(r_min, r_max + 1, r_step):
            x_r_prob = r.cdf(x_r + 1) - r.cdf(x_r)
            y_values[x_l + x_r - y_min] += x_l_prob * x_r_prob
            y_values[x_l + x_r - y_min + 1] += x_l_prob * x_r_prob
    return NumericDistribution(y_values, offset=y_min)


def dist_scale(dist, scale):
    """Return a distribution whose values are scaled by @p scale."""

    if scale == 0:
        return ZERO

    class ScaleWrapper(Distribution):
        """A distribution that scales another distribution along its x
        axis."""
        def __init__(self, parent, _scale):
            self._parent = parent
            self._scale = _scale

        def cdf(self, x):
            return self._parent.cdf(x / self._scale)

        def pdf(self, x):
            return self._parent.pdf(x / self._scale) / self._scale

        def point_on_curve(self):
            return self._parent.point_on_curve() * self._scale

        def quantile(self, p):
            return self._parent.quantile(p) * self._scale

        def contains_point_masses(self):
            return self._parent.contains_point_masses()

    return ScaleWrapper(dist, scale)


def dist_truncate(dist, max_value):
    """Return a distribution that is truncated (ie, right tail rolled up) to
    not exceed @p max_value.  This is used to model, eg, a "timeboxed" task
    that will be abandoned if it exceeds some maximum resource level."""

    assert max_value >= 0
    if max_value == 0:
        return ZERO

    class TruncateWrapper(Distribution):
        """A distribution that truncates another distribution at a specified
        maximum value."""
        def __init__(self, parent, _max_value):
            self._parent = parent
            self._max_value = _max_value
            self._probability_of_success = self._parent.cdf(self._max_value)

        def cdf(self, x):
            return 1. if x >= self._max_value else self._parent.cdf(x)

        def pdf(self, x):
            return (0. if x > self._max_value else
                    float("inf") if x == self._max_value else
                    self._parent.pdf(x))

        def point_on_curve(self):
            return self._parent.point_on_curve()

        def quantile(self, p):
            return (self._max_value if p >= self._probability_of_success
                    else self._parent.quantile(p))

        def contains_point_masses(self):
            return True

    return TruncateWrapper(dist, max_value)
