#! /usr/bin/env python3

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

from distributions.log_logistic import LogLogistic
from distributions.point_distribution import PointDistribution
from distributions.uniform import UniformDistribution
from distributions.numeric import NumericDistribution

import math
from nose_parameterized import parameterized
import unittest

distributions_to_test = [[dut] for dut in (
    LogLogistic(10, 0.5),
    LogLogistic(10, 1),
    LogLogistic(10, 2),
    PointDistribution({2: 1}),
    UniformDistribution(0, 3),
    UniformDistribution(1, 1.4),
    NumericDistribution([1, 4, 6, 4, 1], offset=500),
    NumericDistribution([16, 9, 4, 1]),
    )]


class DistributionRulesTest(unittest.TestCase):

    @parameterized.expand(distributions_to_test)
    def test_negative_t(self, dut):
        neg_inf = float("-inf")
        for t in [neg_inf, -10, -1, -0.1]:
            self.assertAlmostEqual(dut.pdf(t), 0)
        for t in [neg_inf, -10, -1, -0.1, 0]:
            self.assertAlmostEqual(dut.cdf(t), 0)

    @parameterized.expand(distributions_to_test)
    def test_large_t(self, dut):
        inf = float("inf")
        if not math.isnan(dut.pdf(inf)):
            self.assertEqual(dut.pdf(inf), 0)
        if not math.isnan(dut.cdf(inf)):
            self.assertEqual(dut.cdf(inf), 1)

    @parameterized.expand(distributions_to_test)
    def test_monotone(self, dut):
        for test_point in range(1000):
            self.assertLessEqual(dut.cdf(test_point),
                                 dut.cdf(test_point + 0.001))
            self.assertLessEqual(dut.cdf(test_point),
                                 dut.cdf(test_point + 1))

    @parameterized.expand(distributions_to_test)
    def test_derivative(self, dut):
        dt = 0.001
        for base_t in range(1000):
            t = base_t + 0.1  # avoid curve transients at 0
            dpdt = (dut.pdf(t) + dut.pdf(t + dt)) / 2
            dp = dut.cdf(t + dt) - dut.cdf(t)
            self.assertAlmostEqual(dpdt, dp / dt, delta=0.001)

    @parameterized.expand(distributions_to_test)
    def test_quantile(self, dut):
        for p in [0.01, 0.1, 0.2, 0.5, 0.8, 0.9, 0.99]:
            t = dut.quantile(p)
            approximated_p = dut.cdf(t)
            epsilon = (
                0.0001 if not dut.contains_point_masses() else dut.pdf(t))
            self.assertAlmostEqual(p, approximated_p, delta=epsilon,
                                   msg=("Failed quantile check at p=%f t=%f" %
                                        (p, t)))


if __name__ == "__main__":
    unittest.main()
