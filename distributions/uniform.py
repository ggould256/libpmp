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

"""Uniform distributions."""

from distributions.distribution import Distribution


class UniformDistribution(Distribution):
    """A distribution in which all values in a certain range are equally
    likely."""

    def __init__(self, min_value, max_value):
        assert min_value < max_value
        self._min = min_value
        self._max = max_value
        self._density = 1 / (max_value - min_value)

    def pdf(self, x):
        if self._min <= x <= self._max:
            return self._density
        else:
            return 0

    def cdf(self, x):
        if x < self._min:
            return 0
        elif x > self._max:
            return 1
        else:
            return self._density * (x - self._min)

    def quantile(self, p):
        return self._min + (p / self._density)

    def point_on_curve(self):
        return (self._min + self._max) / 2
