#! /usr/bin/env python3

"""Tests for operations module."""

# Tests can be sloppy about variable names; it's no big deal.
# pylint: disable = invalid-name

import unittest

import libpmp.distributions.operations as op
from libpmp.distributions.log_logistic import LogLogistic
from libpmp.distributions.numeric import NumericDistribution
from libpmp.distributions.uniform import UniformDistribution


class DistributionRulesTest(unittest.TestCase):
    """Test some simple invariants on some distributions."""

    def verify_dist_points(self, dist, pdf_points, cdf_points, offset=0):
        """Test that a given distribution @p dist has the PDF and CDF
        described by @p pdf_points, @p cdf_points at the specified
        @p offset."""
        for i in range(len(pdf_points or [])):
            self.assertAlmostEqual(dist.pdf(offset + i), pdf_points[i])
        for i in range(len(cdf_points or [])):
            self.assertAlmostEqual(dist.cdf(offset + i), cdf_points[i])

    def test_add_uniform(self):
        """Test that the sum of two uniform distributions is a triangle."""
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
        """Test that scale does what it says."""
        base = LogLogistic(10, 2)
        scaled = op.dist_scale(base, 2)
        for i in range(2000):
            self.assertEqual(base.pdf(i / 100.), scaled.pdf(i / 50.) * 2)
            self.assertEqual(base.cdf(i / 100.), scaled.cdf(i / 50.))

    def test_truncate(self):
        """Test that truncate does what it says."""
        base = UniformDistribution(1, 5)
        truncated = op.dist_truncate(base, 3)
        self.verify_dist_points(truncated,
                                [0, 0.25, 0.25, float("inf"), 0, 0],
                                [0, 0, 0.25, 1., 1., 1.])


if __name__ == "__main__":
    unittest.main()
