# Copyright 2016 Grant Gould, 2016
# This software is provided under the MIT license, a copy of which is
# available in the LICENSE file of this project.

TESTS = distributions/test/distribution_test.py
TEST_RESULTS = $(TESTS:.py=.result)

all: test

%.result : %.py
	PYTHONPATH=. $<

.PHONY: test
test: $(TEST_RESULTS)
