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

import scipy.optimize

from distributions.distribution import Distribution


def _log_logistic_cdf(x, a, b):
    """See https://en.wikipedia.org/wiki/Log-logistic_distribution"""
    # Use variable names 'x', 'a', and 'b' for comparability to wikipedia.
    if x <= 0:
        return 0
    return 1 / (1 + (x / a) ** -b)


class LogLogistic(Distribution):
    """Log-logistic distribution.  This distribution empirically fits the
    time cost of many software projects and has an easy algebraic CDF, PDF,
    and quantile function that allows scipy to do quick and easy curve fitting
    from multipoint estimates."""

    def __init__(self, alpha, beta):
        """Creates a log-logistic distribution of the given parameters.
        See https://en.wikipedia.org/wiki/Log-logistic_distribution for
        definitions of the parameters."""
        self._alpha = alpha
        self._beta = beta

    def pdf(self, x):
        # Use variable names 'x', 'a', and 'b' for comparability to wikipedia.
        a = self._alpha
        b = self._beta
        if x <= 0:
            return 0
        return ((b / a) * (x / a) ** (b - 1) /
                (1 + (x / a) ** b) ** 2)

    def cdf(self, x):
        return _log_logistic_cdf(x, self._alpha, self._beta)

    def point_on_curve(self):
        return self._alpha

    def quantile(self, p):
        # Use variable names 'a' and 'b' for comparability to wikipedia.
        a = self._alpha
        b = self._beta
        return a * (p / (1 - p)) ** (1 / b)

    @staticmethod
    def fit(first_quantile_p, first_quantile_x,
            second_quantile_p, second_quantile_x):
        """Fit a log-logistic curve to the given fractions.  For instance if
        you want a curve with 8 as its 10th percentile and 40 as its 75th
        percentile, you would call fit(0.1, 8, 0.75, 40)."""
        assert (0 < first_quantile_p < second_quantile_p < 1), (
            "Quantile fractions out of order: 0 < %f < %f < 1" %
            (first_quantile_p, second_quantile_p))
        assert (0 < first_quantile_x < second_quantile_x), (
            "Quantile positions out of order: 0 < %f < %f" %
            (first_quantile_x, second_quantile_x))

        start = [0.5 * (first_quantile_x + second_quantile_x), 1]

        def error(ab):
            a, b = ab
            return (
                (_log_logistic_cdf(first_quantile_x, a, b) -
                 first_quantile_p) ** 2 +
                (_log_logistic_cdf(second_quantile_x, a, b) -
                 second_quantile_p) ** 2)

        def debug_log(ab):
            a, b = ab
            dist = LogLogistic(a, b)
            print("Iterating: a =", a, " b =", b, " e =", error(ab))
            print("Fit: ",
                  dist.quantile(first_quantile_p), " vs ", first_quantile_x,
                  dist.quantile(second_quantile_p), " vs ", second_quantile_x)

        # Add callback=debug_log to debug solver convergence.
        result = scipy.optimize.fmin_bfgs(error, x0=start, disp=0)

        alpha, beta = result
        assert alpha > 0, "fitting of %f:%f %f:%f yielded alpha of %s" % (
            first_quantile_p, first_quantile_x,
            second_quantile_p, second_quantile_x,
            alpha)
        assert beta >= 0, "fitting of %f:%f %f:%f yielded beta of %s" % (
            first_quantile_p, first_quantile_x,
            second_quantile_p, second_quantile_x,
            beta)

        return LogLogistic(alpha, beta)
