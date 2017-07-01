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

TESTS = distributions/test/distribution_test.py \
        distributions/test/operations_test.py \
        model/test/markdown_test.py

TEST_RESULTS = $(TESTS:.py=.result)

all: test check_deps

.PHONY: check_deps
check_deps : python_requirements.txt
	! (pip3 freeze | diff - $< | grep '^>')

%.result : %.py
	PYTHONPATH=. $<

.PHONY: test
test: $(TEST_RESULTS)
