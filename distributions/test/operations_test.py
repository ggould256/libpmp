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
import distributions.operations as op
from distributions.uniform import UniformDistribution
from distributions.numeric import NumericDistribution

import unittest


class DistributionRulesTest(unittest.TestCase):

    def verify_dist_points(self, dist, pdf_points, cdf_points, offset=0):
        for i in range(len(pdf_points or [])):
            self.assertAlmostEqual(dist.pdf(offset + i), pdf_points[i])
        for i in range(len(cdf_points or [])):
            self.assertAlmostEqual(dist.cdf(offset + i), cdf_points[i])

    def test_add_uniform(self):
        u1 = UniformDistribution(0, 1)
        u1twice = op.dist_add(u1, u1)
        self.assertEqual(type(u1twice), NumericDistribution)
        self.verify_dist_points(u1twice, [0.5, 0.5, 0], [0, 0.5, 1])

        u2 = UniformDistribution(1, 3)
        u2twice = op.dist_add(u2, u2)
        self.assertEqual(type(u2twice), NumericDistribution)
        self.verify_dist_points(u2twice,
                                [0.125, 0.375, 0.375, 0.125, 0],
                                [0, 0.125, 0.5, 0.875, 1, 1],
                                offset=2)

    def test_scale(self):
        base = LogLogistic(10, 2)
        scaled = op.dist_scale(base, 2)
        for i in range(2000):
            self.assertEqual(base.pdf(i / 100.), scaled.pdf(i / 50.) * 2)
            self.assertEqual(base.cdf(i / 100.), scaled.cdf(i / 50.))


if __name__ == "__main__":
    unittest.main()
