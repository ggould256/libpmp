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

import math
from distributions.distribution import Distribution


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

    BEFORE, AFTER = [-3, -2]

    def _bucket(self, x):
        if x < self._offset:
            return self.BEFORE
        try:
            bucket = math.floor(x) - self._offset
        except OverflowError as e:
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
