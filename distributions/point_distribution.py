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

from distributions.distribution import Distribution

class PointDistribution(Distribution):
    """Class representing a distribution that can take only a number of
    discrete values with associated probabilities."""

    def __init__(self, value_probabilities):
        """@p value_probabilities is a dict of {value: probability}.  If the
        probabilities do not sum to 1, they will be rescaled."""
        self._values = sorted(value_probabilities.keys())
        assert self._values
        scale = sum(value_probabilities.values())
        self._probabilities = {key: value_probabilities[key] / scale
                               for key in self._values}

    def pdf(self, x):
        return float("inf") if x in self._probabilities else 0

    def cdf(self, x):
        total_probability = 0
        for value in self._values:
            if x < value:
                return total_probability
            else:
                total_probability += self._probabilities[value]
        return 1

    def point_on_curve(self):
        return (self._values[0] + self._values[-1]) / 2

    def quantile(self, p):
        assert 0 <= p <= 1
        total_probability = 0
        for value in self._values:
            total_probability += self._probabilities[value]
            if total_probability >= p:
                return value
        return self._values[-1]

    def contains_point_masses(self):
        return True
